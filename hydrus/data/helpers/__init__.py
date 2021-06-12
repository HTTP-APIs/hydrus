"""
Pluggable utilities for data operations.
=======================================
This module is for generic data-related helpers. For server-related
 utilities use `hydrus.utils`.

Other specific data helpers are in other modules in the same package.
"""

from typing import Dict, Any, List, Optional, Union, Tuple

from flask import Response, jsonify

import re

from hydrus.data import crud

from hydrus.utils import (
    get_doc,
    get_api_name,
    set_response_headers,
    get_session,
    error_response,
)
from hydra_python_core.doc_writer import HydraIriTemplate, IriTemplateMapping, HydraLink
from hydra_python_core.doc_writer import HydraError, DocUrl
from hydrus.extensions.socketio_factory import socketio
from hydrus.conf import get_host_domain


def validObject(object_: Dict[str, Any]) -> bool:
    """
    Check if the Dict passed in POST is of valid format or not.
        (if there's an "@type" key in the dict)
    :param object_ - Object to be checked
    :return : <bool> True if Object has "@type" key
    """
    if "@type" in object_:
        return True
    return False


def validObjectList(objects_: List[Dict[str, Any]]) -> bool:
    """
    Check if the List of Dicts passed are of the valid format or not.
        (if there's an "@type" key in the dict)
    :param objects_: Object to be checked
    :return : <bool> True if all the Object in the List of Dicts have "@type" key
    """
    for object_ in objects_:
        if "@type" not in object_:
            return False
    return True


def get_iri_from_int_list(path_url: str, int_list: List[str]) -> List[str]:
    """Returns a list of full IRIs of multiple objects from int_list
    :param path_url: The path of the object
    :param int_list: Optional String containing ',' separated ID's
    :return: IRIs of multiple objects
    """
    iri_list = []
    for id_ in int_list:
        iri_list.append(f"{path_url}/{id_}")
    return iri_list


def type_match(object_: List[Dict[str, Any]], obj_type: str) -> bool:
    """
    Checks if the object type matches for every object in list.
    :param object_: List of objects
    :param obj_type: The required object type
    :return: True if all object of list have the right type
            False otherwise
    """
    for obj in object_:
        if obj["@type"] != obj_type:
            return False
    return True


def hydrafy(object_: Dict[str, Any], path: Optional[str]) -> Dict[str, Any]:
    """
    Add hydra context to objects.
    :param object_ : Object.
    :param path : Path of the collection or non-collection class .
    :return : object with hydra context
    """
    if path == object_["@type"]:
        object_[
            "@context"
        ] = f"{get_host_domain()}/{get_api_name()}/contexts/{object_['@type']}.jsonld"
    else:
        object_[
            "@context"
        ] = f"{get_host_domain()}/{get_api_name()}/contexts/{path}.jsonld"
    return object_


def checkEndpoint(method: str, path: str) -> Dict[str, Union[bool, int]]:
    """
    Check if endpoint and method is supported in the API.
    :param method: Method name
    :param path: Path of the collection or non-collection class
    :return : Dict with 'method' and 'status' key
    """
    status_val = 404
    vocab_route = get_doc().doc_name
    if path == vocab_route:
        return {"method": False, "status": 405}
    expanded_base_url = DocUrl.doc_url
    for endpoint in get_doc().entrypoint.entrypoint.supportedProperty:
        expanded_endpoint_id = endpoint.id_.replace("EntryPoint/", "")
        endpoint_id = expanded_endpoint_id.split(expanded_base_url)[1]
        if path == endpoint_id:
            status_val = 405
            for operation in endpoint.supportedOperation:
                if operation.method == method:
                    status_val = 200
                    return {"method": True, "status": status_val}
    return {"method": False, "status": status_val}


def getType(class_path: str, method: str) -> Any:
    """
    Return the @type of object allowed for POST/PUT.
    :param class_path: path for the class
    :param method: Method name
    """
    expanded_base_url = DocUrl.doc_url
    for supportedOp in get_doc().parsed_classes[class_path]["class"].supportedOperation:
        if supportedOp.method == method:
            class_type = supportedOp.expects.split(expanded_base_url)[1]
            return class_type


def checkClassOp(path: str, method: str) -> bool:
    """
    Check if the Class supports the operation.
    :param path: Path of the collection or non-collection class.
    :param method: Method name.
    :return: True if the method is defined, false otherwise.
    """
    collections, parsed_classes = get_collections_and_parsed_classes()
    if path in collections:
        supported_operations = (
            get_doc().collections[path]["collection"].supportedOperation
        )
    else:
        supported_operations = (
            get_doc().parsed_classes[path]["class"].supportedOperation
        )
    for supportedOp in supported_operations:
        if supportedOp.method == method:
            return True
    return False


def check_required_props(path: str, obj: Dict[str, Any]) -> bool:
    """
    Check if the object contains all required properties.
    :param path: Path of the collection or non-collection class.
    :param obj: object under check
    :return: True if the object contains all required properties
             False otherwise.
    """
    collections, parsed_classes = get_collections_and_parsed_classes()
    if path in collections:
        # path is of a collection class
        supported_properties = (
            get_doc().collections[path]["collection"].supportedProperty
        )
    else:
        # path is of a non-collection class
        supported_properties = get_doc().parsed_classes[path]["class"].supportedProperty
    for prop in supported_properties:
        if prop.required:
            if prop.title not in obj:
                return False
    return True


def check_writeable_props(path: str, obj: Dict[str, Any]) -> bool:
    """
    Check that the object only contains writeable fields(properties).
    :param path: Path of the collection or non-collection class.
    :param obj: object under check
    :return: True if the object only contains writeable properties
             False otherwise.
    """
    collections, parsed_classes = get_collections_and_parsed_classes()
    if path in collections:
        # path is of a collection class
        supported_properties = (
            get_doc().collections[path]["collection"].supportedProperty
        )
    else:
        # path is of a non-collection class
        supported_properties = get_doc().parsed_classes[path]["class"].supportedProperty
    for prop in supported_properties:
        if prop.write is False:
            if prop.title in obj:
                return False
    return True


def get_nested_class_path(class_type: str) -> Tuple[str, bool]:
    """
    Get the path of class
    :param class_type: class name whose path is needed
    :return: Tuple, where the first element is the path string and
             the second element is a boolean, True if the class is a collection class
             False otherwise.
    """
    expanded_base_url = DocUrl.doc_url
    collections, parsed_classes = get_collections_and_parsed_classes()
    for path in collections:
        collection = collections[path]["collection"]
        class_name = collection.manages["object"].split(expanded_base_url)[1]
        collection_manages_class = parsed_classes[class_name]["class"]
        collection_manages_class_type = collection_manages_class.title
        collection_manages_class_path = collection_manages_class.path
        if collection_manages_class_type == class_type:
            return collection_manages_class_path, True
    for class_path in parsed_classes:
        if class_type == parsed_classes[class_path]["class"].title:
            return class_path, False


def finalize_response(path: str, obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    finalize response objects by removing properties which are not readable and correcting path
    of nested objects.
    :param path: Path of the collection or non-collection class.
    :param obj: object being finalized
    :return: An object not containing any `readable=False` properties and having proper path
             of any nested object's url.
    """
    collections, parsed_classes = get_collections_and_parsed_classes()
    expanded_base_url = DocUrl.doc_url
    if path in collections:
        members = list()
        for member in obj["members"]:
            member_id = member[0]
            member_type = member[1]
            member_path = get_path_from_type(member_type)
            member = {
                "@type": "hydra:Link",
                "@id": f"{get_host_domain()}/{get_api_name()}/{member_path}/{member_id}",
            }
            members.append(member)
        obj["members"] = members
        return obj
    else:
        # path is of a non-collection class
        supported_properties = get_doc().parsed_classes[path]["class"].supportedProperty
        expanded_base_url = DocUrl.doc_url
        for prop in supported_properties:
            # Skip not required properties which are not inserted yet.
            if not prop.required and prop.title not in obj:
                continue
            # if prop.read is False:
            #     obj.pop(prop.title, None)
            elif isinstance(prop.prop, HydraLink):
                hydra_link = prop.prop
                range_class = hydra_link.range.split(expanded_base_url)[1]
                nested_path, is_collection = get_nested_class_path(range_class)
                if is_collection:
                    id = obj[prop.title]
                    obj[prop.title] = f"/{get_api_name()}/{nested_path}/{id}"
                else:
                    obj[prop.title] = f"/{get_api_name()}/{nested_path}"
            elif expanded_base_url in prop.prop:
                prop_class = prop.prop.split(expanded_base_url)[1]
                prop_class_path = parsed_classes[prop_class]["class"].path
                id = obj[prop.title]
                class_resp = crud.get(
                    id, prop_class, get_api_name(), get_session(), path=prop_class_path
                )
                obj[prop.title] = finalize_response(prop_class_path, class_resp)
        return obj


def add_iri_template(path: str, API_NAME: str, collection_path: str) -> Dict[str, Any]:
    """
    Creates an IriTemplate.
    :param path: Path of the collection or the non-collection class.
    :param API_NAME: Name of API.
    :return: Hydra IriTemplate .
    """
    template_mappings = list()
    template = f"/{API_NAME}/{collection_path}{{?"
    template, template_mappings = generate_iri_mappings(
        path,
        template,
        template_mapping=template_mappings,
    )

    template, template_mappings = add_pagination_iri_mappings(
        template=template, template_mapping=template_mappings
    )
    return HydraIriTemplate(template=template, iri_mapping=template_mappings).generate()


def generate_iri_mappings(
    path: str,
    template: str,
    skip_nested: bool = False,
    template_mapping: List[IriTemplateMapping] = [],
    parent_prop_name: str = None,
) -> Tuple[str, List[IriTemplateMapping]]:
    """
    Generate iri mappings to add to IriTemplate
    :param path: Path of the collection or non-collection class.
    :param template: IriTemplate string.
    :param skip_nested: To only add properties of the class_type class or
                        its immediate children.
    :param template_mapping: List of template mappings.
    :param parent_prop_name: Property name according to parent object
                             (only applies for nested properties)
    :return: Template string, list of template mappings and boolean showing whether
             to keep adding delimiter or not.
    """
    expanded_base_url = DocUrl.doc_url
    for supportedProp in get_doc().parsed_classes[path]["class"].supportedProperty:
        prop_class = supportedProp.prop
        nested_class_prop = False
        if isinstance(supportedProp.prop, HydraLink):
            hydra_link = supportedProp.prop
            prop_class = hydra_link.range.split(expanded_base_url)[1]
            nested_class_prop = True
        elif expanded_base_url in supportedProp.prop:
            prop_class = supportedProp.prop.split(expanded_base_url)[1]
            nested_class_prop = True
        if nested_class_prop and skip_nested is False:
            template, template_mapping = generate_iri_mappings(
                prop_class,
                template,
                skip_nested=True,
                parent_prop_name=supportedProp.title,
                template_mapping=template_mapping,
            )
            continue
        if skip_nested is True:
            var = f"{parent_prop_name}[{supportedProp.title}]"
            mapping = IriTemplateMapping(variable=var, prop=prop_class)
        else:
            var = supportedProp.title
            mapping = IriTemplateMapping(variable=var, prop=prop_class)
        template_mapping.append(mapping)
        template = template + f"{var}, "
    return template, template_mapping


def add_pagination_iri_mappings(
    template: str, template_mapping: List[IriTemplateMapping]
) -> Tuple[str, List[IriTemplateMapping]]:
    """
    Add various pagination related to variable to the IRI template and also adds mappings for them.
    :param template: IriTemplate string.
    :param template_mapping: List of template mappings.
    :return: Final IriTemplate string and related list of mappings.
    """
    paginate_variables = ["pageIndex", "limit", "offset"]
    for i in range(len(paginate_variables)):
        # If final variable then do not add space and comma and add the final parentheses
        if i == len(paginate_variables) - 1:
            template += f"{paginate_variables[i]}}}"
        else:
            template += f"{paginate_variables[i]}, "
        mapping = IriTemplateMapping(
            variable=paginate_variables[i], prop=paginate_variables[i]
        )
        template_mapping.append(mapping)
    return template, template_mapping


def send_sync_update(
    socketio, new_job_id: int, last_job_id: str, method: str, resource_url: str
):
    """
    Sends synchronization update to all connected clients.
    :param socketio: socketio connection.
    :param new_job_id: Job id of the new modification(update).
    :param last_job_id: Job id of the last(most recent) modification until this new one.
    :param method: Method type of the operation.
    :param resource_url: URL of resource which needs to be synchronized.
    """
    data = {
        "job_id": new_job_id,
        "last_job_id": last_job_id,
        "method": method,
        "resource_url": resource_url,
    }
    socketio.emit("update", data, namespace="/sync")


def get_link_props(path: str, object_) -> Tuple[Dict[str, Any], bool]:
    """
    Get dict of all hydra_link properties of a class.
    :param path: Path of the collection or non-collection class.
    :param object_: Object being inserted/updated.
    :return: Tuple with one elements as Dict with property_title as key and
             instance_id(for collection class) or class_name(for non-collection class) as value,
             second element represents boolean representing validity of the link.
    """
    link_props = {}
    collections, parsed_classes = get_collections_and_parsed_classes()
    expanded_base_url = DocUrl.doc_url
    if path in collections:
        # path is of a collection class
        supported_properties = (
            get_doc().collections[path]["collection"].supportedProperty
        )
    else:
        # path is of a non-collection class
        supported_properties = get_doc().parsed_classes[path]["class"].supportedProperty
    for supportedProp in supported_properties:
        if isinstance(supportedProp.prop, HydraLink) and supportedProp.title in object_:
            prop_range = supportedProp.prop.range
            range_class_name = prop_range.split(expanded_base_url)[1]
            for collection_path in get_doc().collections:
                if collection_path in object_[supportedProp.title]:
                    class_title = (
                        get_doc()
                        .collections[collection_path]["collection"]
                        .class_.title
                    )
                    if range_class_name != class_title:
                        return {}, False
                    link_props[supportedProp.title] = object_[
                        supportedProp.title
                    ].split("/")[-1]
                    break
            if supportedProp.title not in link_props:
                for class_path in get_doc().parsed_classes:
                    if class_path in object_[supportedProp.title]:
                        class_title = (
                            get_doc().parsed_classes[class_path]["class"].title
                        )
                        if range_class_name != class_title:
                            return {}, False
                        link_props[supportedProp.title] = class_title
                        break
    return link_props, True


def get_link_props_for_multiple_objects(
    path: str, object_list: List[Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], bool]:
    """
    Get link_props of multiple objects.
    :param path: Path of the collection or non-collection class.
    :param object_list: List of objects being inserted.
    :return: List of link properties processed with the help of get_link_props.
    """
    link_prop_list = list()
    for object_ in object_list:
        link_props, type_check = get_link_props(path, object_)
        if type_check is True:
            link_prop_list.append(link_props)
        else:
            return [], False
    return link_prop_list, True


def validate_object(object_: Dict[str, Any], obj_type: str, class_path: str) -> bool:
    """
    Check if the object dict passed in POST can be inserted/updated
    in database.

    :param object_: Object to be checked
    :param obj_type: The required object type
    :param class_path: Path of the class
    :return: True if the object is completely valid
    """
    return (
        validObject(object_) and
        object_["@type"] == obj_type and
        check_required_props(class_path, object_)
    )


def get_context(category: str) -> Response:
    """
    Generate the context for a given category.

    :param category: The category of class for which context is required
    :type category: str
    :return: Response with context
    :rtype: Response
    """
    collections, parsed_classes = get_collections_and_parsed_classes()
    # Check for collection
    if category in get_doc().collections:
        # type: Union[Dict[str,Any],Dict[int,str]]
        response = {"@context": collections[category]["context"].generate()}
        return set_response_headers(jsonify(response))
    # Check for non collection class
    elif category in parsed_classes:
        response = {
            "@context": get_doc().parsed_classes[category]["context"].generate()
        }
        return set_response_headers(jsonify(response))
    else:
        error = HydraError(code=404, title="NOT FOUND", desc="Context not found")
        return error_response(error)


def get_path_from_type(type_: str) -> str:
    _, parsed_classes = get_collections_and_parsed_classes()
    expanded_base_url = DocUrl.doc_url
    for class_name in parsed_classes:
        class_ = parsed_classes[class_name]["class"]
        if type_ == class_.id_.split(expanded_base_url)[1]:
            return class_.path


def parse_collection_members(object_: dict) -> dict:
    """Parse the members of a collection to make it easier
    to insert in database.

    :param object_: The body of the request having object members
    :type object_: dict
    :return: Object with parsed members
    :rtype: dict
    """
    members = list()
    for member in object_["members"]:
        # example member
        # {
        #     "@id": "/serverapi/LogEntry/aab38f9d-516a-4bb2-ae16-068c0c5345bd",
        #     "@type": "LogEntry"
        # }
        member_id = member["@id"].split("/")[-1]
        member_type = member["@type"]
        if crud.item_exists(member_type, member_id, get_session()):
            members.append(
                {
                    "id_": member_id,
                    "@type": member_type,
                }
            )
        else:
            error = HydraError(code=400, title="Data is not valid")
            return error_response(error)
    object_["members"] = members
    return object_


def get_fragments(resource: str) -> dict:
    """Gets a fragment of the main hydra vocabulary.

    :param resource: Fragment specified in the request parameters
    :type resource: str
    :return: Object referred to by the fragment
    :rtype: dict
    """
    resource_dict = dict()
    gen_doc = get_doc().generate()
    if "EntryPoint/" in resource:
        match_string = r"\b(EntryPoint)\b"
        for class_ in gen_doc["supportedClass"]:
            if re.search(match_string, class_["@id"]):
                res = class_
                break
        for properties in res["supportedProperty"]:
            if resource in properties["property"]["@id"]:
                res = properties
                break
        resource_dict[resource[11:]] = res
    else:
        resource_dict["@context"] = gen_doc["@context"]
        for class_ in gen_doc["supportedClass"]:
            match_string = r"\b({0})\b".format(resource)
            if re.search(match_string, class_["@id"]):
                res = class_
                break
        resource_dict["supportedClass"] = [res]
    return resource_dict


def get_collections_and_parsed_classes():
    """
    Get all the collections and parsed classes from
    the API doc.
    :return collections, parsed_classes
            <tuple>
    """
    api_doc = get_doc()
    parsed_classes = api_doc.parsed_classes
    collections = api_doc.collections
    return (collections, parsed_classes)
