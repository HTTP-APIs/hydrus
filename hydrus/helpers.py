from typing import Dict, Any, List, Optional, Union, Tuple

from flask import Response

from hydrus.data import crud

from hydrus.utils import get_doc, get_api_name, get_hydrus_server_url, get_session

from hydra_python_core.doc_writer import HydraIriTemplate, IriTemplateMapping, HydraLink


def validObject(object_: Dict[str, Any]) -> bool:
    """
        Check if the Dict passed in POST is of valid format or not.
        (if there's an "@type" key in the dict)

        :param object_ - Object to be checked
    """
    if "@type" in object_:
        return True
    return False


def validObjectList(objects_: List[Dict[str, Any]]) -> bool:
    """
        Check if the List of Dicts passed are of the valid format or not.
        (if there's an "@type" key in the dict)

    :param objects_: Object to be checked
    """
    for object_ in objects_:
        if "@type" not in object_:
            return False
    return True


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


def set_response_headers(resp: Response,
                         ct: str = "application/ld+json",
                         headers: List[Dict[str, Any]]=[],
                         status_code: int = 200) -> Response:
    """Set the response headers."""
    resp.status_code = status_code
    for header in headers:
        resp.headers[list(header.keys())[0]] = header[list(header.keys())[0]]
    resp.headers['Content-type'] = ct
    link = "http://www.w3.org/ns/hydra/core#apiDocumentation"
    resp.headers['Link'] = '<{}{}/vocab>; rel="{}"'.format(
        get_hydrus_server_url(), get_api_name(), link)
    return resp


def hydrafy(object_: Dict[str, Any], path: Optional[str]) -> Dict[str, Any]:
    """Add hydra context to objects."""
    if path == object_["@type"]:
        object_[
            "@context"] = "/{}/contexts/{}.jsonld".format(get_api_name(), object_["@type"])
    else:
        object_[
            "@context"] = "/{}/contexts/{}.jsonld".format(get_api_name(), path)
    return object_


def checkEndpoint(method: str, path: str) -> Dict[str, Union[bool, int]]:
    """Check if endpoint and method is supported in the API."""
    status_val = 404
    if path == 'vocab':
        return {'method': False, 'status': 405}

    for endpoint in get_doc().entrypoint.entrypoint.supportedProperty:
        if path == "/".join(endpoint.id_.split("/")[1:]):
            status_val = 405
            for operation in endpoint.supportedOperation:
                if operation.method == method:
                    status_val = 200
                    return {'method': True, 'status': status_val}
    return {'method': False, 'status': status_val}


def getType(class_path: str, method: str) -> Any:
    """Return the @type of object allowed for POST/PUT."""
    for supportedOp in get_doc(
    ).parsed_classes[class_path]["class"].supportedOperation:
        if supportedOp.method == method:
            return supportedOp.expects.replace("vocab:", "")
    # NOTE: Don't use split, if there are more than one substrings with
    # 'vocab:' not everything will be returned.


def checkClassOp(class_type: str, method: str) -> bool:
    """Check if the Class supports the operation."""
    for supportedOp in get_doc(
    ).parsed_classes[class_type]["class"].supportedOperation:
        if supportedOp.method == method:
            return True
    return False


def check_required_props(class_type: str, obj: Dict[str, Any]) -> bool:
    """
    Check if the object contains all required properties.
    :param class_type: class name of the object
    :param obj: object under check
    :return: True if the object contains all required properties
             False otherwise.
    """
    for prop in get_doc().parsed_classes[class_type]["class"].supportedProperty:
        if prop.required:
            if prop.title not in obj:
                return False
    return True


def check_writeable_props(class_type: str, obj: Dict[str, Any]) -> bool:
    """
    Check that the object only contains writeable fields(properties).
    :param class_type: class name of the object
    :param obj: object under check
    :return: True if the object only contains writeable properties
             False otherwise.
    """
    for prop in get_doc().parsed_classes[class_type]["class"].supportedProperty:
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
    for collection in get_doc().collections:
        if get_doc().collections[collection]["collection"].class_.title == class_type:
            return get_doc().collections[collection]["collection"].path, True

    return get_doc().parsed_classes[class_type]["class"].path, False


def finalize_response(class_type: str, obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    finalize response objects by removing properties which are not readable and correcting path
    of nested objects.
    :param class_type: class name of the object
    :param obj: object being finalized
    :return: An object not containing any `readable=False` properties and having proper path
             of any nested object's url.
    """
    for prop in get_doc().parsed_classes[class_type]["class"].supportedProperty:
        # Skip not required properties which are not inserted yet.
        if not prop.required and prop.title not in obj:
            continue
        if prop.read is False:
            obj.pop(prop.title, None)
        elif isinstance(prop.prop, HydraLink):
            hydra_link = prop.prop
            range_class = hydra_link.range.replace("vocab:", "")
            nested_path, is_collection = get_nested_class_path(range_class)
            if is_collection:
                id = obj[prop.title]
                obj[prop.title] = "/{}/{}/{}".format(get_api_name(), nested_path, id)
            else:
                obj[prop.title] = "/{}/{}".format(get_api_name(), nested_path)
        elif 'vocab:' in prop.prop:
            prop_class = prop.prop.replace("vocab:", "")
            id = obj[prop.title]
            obj[prop.title] = crud.get(id, prop_class, get_api_name(), get_session())
    return obj


def add_iri_template(class_type: str, API_NAME: str, path: str) -> Dict[str, Any]:
    template_mappings = list()
    template = "/{}/{}(".format(API_NAME, path)
    first = True
    template, template_mappings = generate_iri_mappings(class_type, template,
                                                        template_mapping=template_mappings,)

    template, template_mappings = add_pagination_iri_mappings(template=template,
                                                              template_mapping=template_mappings)
    return HydraIriTemplate(template=template, iri_mapping=template_mappings).generate()


def generate_iri_mappings(class_type: str, template: str, skip_nested: bool = False,
                          template_mapping: List[IriTemplateMapping] = [],
                          parent_prop_name: str = None) -> Tuple[str, List[IriTemplateMapping]]:
    """Generate iri mappings to add to IriTemplate
    :param class_type: class name objects contained in collection.
    :param template: IriTemplate string.
    :param skip_nested: To only add properties of the class_type class or
                        its immediate children.
    :param template_mapping: List of template mappings.
    :param parent_prop_name: Property name according to parent object
                             (only applies for nested properties)
    :return: Template string, list of template mappings and boolean showing whether
             to keep adding delimiter or not.
    """
    for supportedProp in get_doc(
    ).parsed_classes[class_type]["class"].supportedProperty:
        prop_class = supportedProp.prop
        nested_class_prop = False
        if isinstance(supportedProp.prop, HydraLink):
            hydra_link = supportedProp.prop
            prop_class = hydra_link.range.replace("vocab:", "")
            nested_class_prop = True
        elif "vocab:" in supportedProp.prop:
            prop_class = supportedProp.prop.replace("vocab:", "")
            nested_class_prop = True
        if nested_class_prop and skip_nested is False:
            template, template_mapping = generate_iri_mappings(prop_class, template,
                                                               skip_nested=True,
                                                               parent_prop_name=supportedProp.title,
                                                               template_mapping=template_mapping)
            continue
        if skip_nested is True:
            var = "{}[{}]".format(parent_prop_name, supportedProp.title)
            mapping = IriTemplateMapping(variable=var, prop=prop_class)
        else:
            var = supportedProp.title
            mapping = IriTemplateMapping(variable=var, prop=prop_class)
        template_mapping.append(mapping)
        template = template + "{}, ".format(var)
    return template, template_mapping


def add_pagination_iri_mappings(template: str,
                                template_mapping: List[IriTemplateMapping]
                                ) -> Tuple[str, List[IriTemplateMapping]]:
    """Add various pagination related to variable to the IRI template and also adds mappings for them.
    :param template: IriTemplate string.
    :param template_mapping: List of template mappings.
    :return: Final IriTemplate string and related list of mappings.
    """
    paginate_variables = ["pageIndex", "limit", "offset"]
    for i in range(len(paginate_variables)):
        # If final variable then do not add space and comma and add the final parentheses
        if i == len(paginate_variables) - 1:
            template += "{})".format(paginate_variables[i])
        else:
            template += "{}, ".format(paginate_variables[i])
        mapping = IriTemplateMapping(variable=paginate_variables[i], prop=paginate_variables[i])
        template_mapping.append(mapping)
    return template, template_mapping


def send_sync_update(socketio, new_job_id: int, last_job_id: str,
                     method: str, resource_url: str):
    """Sends synchronization update to all connected clients.
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
        "resource_url": resource_url
    }
    socketio.emit('update', data, namespace="/sync")


def get_link_props(class_type: str, object_) -> Tuple[Dict[str, Any], bool]:
    """
    Get dict of all hydra_link properties of a class.
    :param class_type: Type of the class.
    :param object_: Object being inserted/updated.
    :return: Tuple with one elements as Dict with property_title as key and
             instance_id(for collection class) or class_name(for non-collection class) as value,
             second element represents boolean representing validity of the link.
    """
    link_props = {}
    for supportedProp in get_doc().parsed_classes[class_type]['class'].supportedProperty:
        if isinstance(supportedProp.prop, HydraLink) and supportedProp.title in object_:
            prop_range = supportedProp.prop.range
            range_class_name = prop_range.replace("vocab:", "")
            for collection_path in get_doc().collections:
                if collection_path in object_[supportedProp.title]:
                    class_title = get_doc().collections[collection_path]['collection'].class_.title
                    if range_class_name != class_title:
                        return {}, False
                    link_props[supportedProp.title] = object_[supportedProp.title].split('/')[-1]
                    break
            if supportedProp.title not in link_props:
                for class_path in get_doc().parsed_classes:
                    if class_path in object_[supportedProp.title]:
                        class_title = get_doc().parsed_classes[class_path]['class'].title
                        if range_class_name != class_title:
                            return {}, False
                        link_props[supportedProp.title] = class_title
                        break
    return link_props, True


def get_link_props_for_multiple_objects(class_type: str,
                                        object_list: List[Dict[str, Any]]
                                        ) -> Tuple[List[Dict[str, Any]], bool]:
    """
    Get link_props of multiple objects.
    :param class_type: Class type of objects.
    :param object_list: List of objects being inserted.
    :return: List of link properties processed with the help of get_link_props.
    """
    link_prop_list = list()
    for object_ in object_list:
        link_props, type_check = get_link_props(class_type, object_)
        if type_check is True:
            link_prop_list.append(link_props)
        else:
            return [], False
    return link_prop_list, True
