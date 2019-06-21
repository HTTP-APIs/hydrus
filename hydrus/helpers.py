from typing import Dict, Any, List, Optional, Union, Tuple

from flask import Response

from hydrus.utils import get_doc, get_api_name, get_hydrus_server_url

from hydra_python_core.doc_writer import HydraIriTemplate, IriTemplateMapping


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


def check_read_only_props(class_type: str, obj: Dict[str, Any]) -> bool:
    """
    Check that the object does not contain any read-only properties.
    :param class_type: class name of the object
    :param obj: object under check
    :return: True if the object doesn't contain any read-only properties
             False otherwise.
    """
    for prop in get_doc().parsed_classes[class_type]["class"].supportedProperty:
        if prop.read:
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
    finalize response objects by removing write-only properties and correcting path
    of nested objects.
    :param class_type: class name of the object
    :param obj: object being finalized
    :return: An object not containing any write-only properties and having proper path
             of any nested object's url.
    """
    for prop in get_doc().parsed_classes[class_type]["class"].supportedProperty:
        if prop.write:
            obj.pop(prop.title, None)
        elif 'vocab:' in prop.prop:
            prop_class = prop.prop.replace("vocab:", "")
            nested_path, is_collection = get_nested_class_path(prop_class)
            if is_collection:
                id = obj[prop.title]
                obj[prop.title] = "/{}/{}/{}".format(get_api_name(), nested_path, id)
            else:
                obj[prop.title] = "/{}/{}".format(get_api_name(), nested_path)
    return obj


def add_iri_template(class_type: str, API_NAME: str, path:str) -> Dict[str, Any]:
    template_mappings = list()
    template = "/{}/{}(".format(API_NAME, path)
    first = True
    template, template_mappings, skip_del = generate_iri_mappings(class_type, template,
                                                                  template_mapping=template_mappings,)
    template += ")"
    return HydraIriTemplate(template=template, iri_mapping=template_mappings).generate()


def generate_iri_mappings(class_type: str, template: str, skip_nested: bool =False, skip_delimiter: bool = True,
                     template_mapping: List[IriTemplateMapping]=[], parent_prop_name: str = None) -> Tuple[str,
                                                                             List[IriTemplateMapping], bool]:
    """Generate iri mappings to add to IriTemplate
    :param class_type: class name objects contained in collection.
    :param template: IriTemplate string.
    :param skip_nested: To only add properties of the class_type class or its immediate children.
    :param skip_delimiter: Used to place delimiters between various parameters of template.
    :param template_mapping: List of template mappings.
    :param parent_prop_name: Property name according to parent object (only applies for nested properties)
    :return: Template string, list of template mappings and boolean showing whether to keep adding
                delimiter or not.
    """
    for supportedProp in get_doc(
    ).parsed_classes[class_type]["class"].supportedProperty:
        if "vocab:" in supportedProp.prop and skip_nested is False:
            prop_class = supportedProp.prop.replace("vocab:", "")
            template, template_mapping, skip_delimiter = generate_iri_mappings(prop_class, template, skip_nested=True,
                                                                               skip_delimiter=skip_delimiter,
                                                                               parent_prop_name=supportedProp.title,
                                                                               template_mapping=template_mapping)
            continue
        if skip_nested is True:
            var = "{}[{}]".format(parent_prop_name, supportedProp.title)
            mapping = IriTemplateMapping(variable=var, prop=supportedProp.prop)
        else:
            var = supportedProp.title
            mapping = IriTemplateMapping(variable=var, prop=supportedProp.prop)
        template_mapping.append(mapping)
        if skip_delimiter is True:
            template = template + "{}".format(var)
            skip_delimiter = False
        else:
            template = template + ", {}".format(var)
    return template, template_mapping, skip_delimiter
