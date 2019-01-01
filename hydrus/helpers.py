from typing import Dict, Any, List, Optional, Union

from flask import Response

from hydrus.utils import get_doc, get_api_name, get_hydrus_server_url


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
    resp.headers['Link'] = '<{}{}/vocab>; rel='
    '"http://www.w3.org/ns/hydra/core#apiDocumentation"'.format(
            get_hydrus_server_url(), get_api_name())
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
