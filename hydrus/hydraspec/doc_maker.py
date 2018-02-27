"""Contsructor to take a Python dict containing an API Documentation and create a HydraDoc object for it."""

from hydrus.hydraspec.doc_writer_sample import api_doc as sample_document
from hydrus.hydraspec.doc_writer import HydraDoc, HydraClass, HydraClassProp, HydraClassOp, HydraStatus
import re
import json
from typing import Any, Dict, Match, Optional, Tuple, Union


def create_doc(doc: Dict[str, Any], HYDRUS_SERVER_URL: str=None, API_NAME: str=None) -> HydraDoc:
    """Create the HydraDoc object from the API Documentation."""
    # Check @id
    try:
        id_ = doc["@id"]
    except KeyError:
        raise SyntaxError("The API Documentation must have [@id]")

    # Extract base_url, entrypoint and API name
    matchObj = re.match(r'(.*)://(.*)/(.*)/vocab#?', id_, re.M | re.I)
    if matchObj:
        base_url = matchObj.group(1) + '://' + matchObj.group(2) + '/'
        entrypoint = matchObj.group(3)

    # Syntax checks
    else:
        raise SyntaxError("The '@id' of the Documentation must be of the form:\n'[protocol] :// [base url] / [entrypoint] / vocab'")
    try:
        desc = doc["description"]
    except KeyError:
        raise SyntaxError("The API Documentation must have [description]")
    try:
        title = doc["title"]
    except KeyError:
        raise SyntaxError("The API Documentation must have [title]")
    try:
        supportedClass = doc["supportedClass"]
    except KeyError:
        raise SyntaxError("The API Documentation must have [supportedClass]")
    try:
        context = doc["@context"]
    except KeyError:
        raise SyntaxError("The API Documentation must have [@context]")
    try:
        possibleStatus = doc["possibleStatus"]
    except KeyError:
        raise SyntaxError("The API Documentation must have [possibleStatus]")

    # EntryPoint object
    entrypoint_obj = get_entrypoint(doc)     # getEntrypoint checks if all classes have @id

    # Main doc object
    if HYDRUS_SERVER_URL is not None and API_NAME is not None:
        apidoc = HydraDoc(API_NAME, title, desc, API_NAME, HYDRUS_SERVER_URL)
    else:
        apidoc = HydraDoc(entrypoint, title, desc, entrypoint, base_url)

    # additional context entries
    for entry in context:
        apidoc.add_to_context(entry, context[entry])

    # add all parsed_classes
    for class_ in supportedClass:
        class_obj, collection = create_class(entrypoint_obj, class_)
        if class_obj:
            apidoc.add_supported_class(class_obj, collection=collection)

    # add possibleStatus
    for status in possibleStatus:
        status_obj = create_status(status)
        apidoc.add_possible_status(status_obj)

    apidoc.add_baseResource()
    apidoc.add_baseCollection()
    apidoc.gen_EntryPoint()
    return apidoc


def create_class(entrypoint: Dict[str, Any], class_dict: Dict[str, Any]) -> Tuple[HydraClass, bool]:
    """Create HydraClass objects for classes in the API Documentation."""
    # Base classes not used
    exclude_list = ['http://www.w3.org/ns/hydra/core#Resource',
                    'http://www.w3.org/ns/hydra/core#Collection',
                    entrypoint["@id"]]
    id_ = class_dict["@id"]
    if id_ in exclude_list:
        return None, None
    matchObj = re.match(r'vocab:(.*)', id_, re.M | re.I)
    if matchObj:
        id_ = matchObj.group(1)

    # Syntax checks
    try:
        supportedProperty = class_dict["supportedProperty"]
    except KeyError:
        raise SyntaxError("Class must have [supportedProperty]")
    try:
        title = class_dict["title"]
    except KeyError:
        raise SyntaxError("Class must have [title]")
    try:
        desc = class_dict["description"]
    except KeyError:
        raise SyntaxError("Class must have [description]")
    try:
        supportedOperation = class_dict["supportedOperation"]
    except KeyError:
        raise SyntaxError("Class must have [supportedOperation]")

    # See if class_dict is a Collection Class
    collection = re.match(r'(.*)Collection(.*)', title, re.M | re.I) #type: Union[Match[Any], bool]
    if collection:
        return None, None

    # Check if class has it's own endpoint
    endpoint = class_in_endpoint(class_dict, entrypoint)

    # Check if class has a Collection
    collection = collection_in_endpoint(class_dict, entrypoint)

    # Create the HydraClass object
    class_ = HydraClass(id_, title, desc, endpoint=endpoint)

    # Add supportedProperty for the Class
    for prop in supportedProperty:
        prop_obj = create_property(prop)
        class_.add_supported_prop(prop_obj)

    # Add supportedOperation for the Class
    for op in supportedOperation:
        op_obj = create_operation(op)
        class_.add_supported_op(op_obj)

    return class_, collection


def get_entrypoint(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Find and return the entrypoint object in the doc."""
    # Search supportedClass
    for class_ in doc["supportedClass"]:
        # Check the @id for each class
        try:
            class_id = class_["@id"]
        except KeyError:
            raise SyntaxError("Each supportedClass must have [@id]")
        # Match with regular expression
        matchObj = re.match(r'vocab:(.*)EntryPoint', class_id)
        # Return the entrypoint object
        if matchObj:
            return class_
    # If not found, raise error
    raise SyntaxError("No EntryPoint class found")


def convert_literal(literal: Any) -> Optional[Union[bool, str]]:
    """Convert JSON literals to Python ones."""
    # Map for the literals
    map_ = {
        "true": True,
        "false": False,
        "null": None
    }
    # Check if literal is in string format
    if type(literal) == str:
        # Check if the literal is valid
        if literal in map_:
            return map_[literal]
        else:
            return literal
    elif isinstance(literal, (bool,)) or literal is None:
        return literal
    else:
        # Raise error for non string objects
        raise TypeError("Literal not recognised")


def create_property(supported_prop: Dict[str, Any]) -> HydraClassProp:
    """Create a HydraClassProp object from the supportedProperty."""
    # Syntax checks
    try:
        uri = supported_prop["property"]
    except KeyError:
        raise SyntaxError("Property must have [property]")
    try:
        title = supported_prop["title"]
    except KeyError:
        raise SyntaxError("Property must have [title]")
    try:
        read = convert_literal(supported_prop["readonly"])
    except KeyError:
        raise SyntaxError("Property must have [readonly]")
    try:
        write = convert_literal(supported_prop["writeonly"])
    except KeyError:
        raise SyntaxError("Property must have [writeonly]")
    try:
        required = convert_literal(supported_prop["required"])
    except KeyError:
        raise SyntaxError("Property must have [required]")
    # Create the HydraClassProp object
    prop = HydraClassProp(uri, title, required=required, read=read, write=write) # type: ignore
    return prop


def class_in_endpoint(class_: Dict[str, Any], entrypoint: Dict[str, Any]) -> bool:
    """Check if a given class is in the EntryPoint object as a class."""
    regex = r'(vocab:)?(.*)EntryPoint/(.*/)?' + re.escape(class_["title"]) + r'$'
    # Check supportedProperty for the EntryPoint
    try:
        supportedProperty = entrypoint["supportedProperty"]
    except KeyError:
        raise SyntaxError("EntryPoint must have [supportedProperty]")

    # Check all endpoints in supportedProperty
    for prop in supportedProperty:
        # Syntax checks
        try:
            property_ = prop["property"]
        except KeyError:
            raise SyntaxError("supportedProperty must have [property]")
        try:
            id_ = property_["@id"]
        except KeyError:
            raise SyntaxError("property must have [@id]")
        # Match the title with regular expression
        matchObj = re.match(regex, id_)
        if matchObj:
            return True
    return False


def collection_in_endpoint(class_: Dict[str, Any], entrypoint: Dict[str, Any]) -> bool:
    """Check if a given class is in the EntryPoint object as a collection."""
    regex = r'(vocab:)?(.*)EntryPoint/(.*/)?' + class_["title"] + "Collection"
    # Check supportedProperty for the EntryPoint
    try:
        supportedProperty = entrypoint["supportedProperty"]
    except KeyError:
        raise SyntaxError("EntryPoint must have [supportedProperty]")

    # Check all endpoints in supportedProperty
    for prop in supportedProperty:
        # Syntax checks
        try:
            property_ = prop["property"]
        except KeyError:
            raise SyntaxError("supportedProperty must have [property]")
        try:
            id_ = property_["@id"]
        except KeyError:
            raise SyntaxError("property must have [@id]")
        # Match the title with regular expression
        matchObj = re.match(regex, id_)
        if matchObj:
            return True
    return False


def create_operation(supported_op: Dict[str, Any]) -> HydraClassOp:
    """Create a HyraClassOp object from the supportedOperation."""
    # Syntax checks
    try:
        name = supported_op["title"]
    except KeyError:
        raise SyntaxError("Operation must have [title]")
    try:
        method = supported_op["method"]
    except KeyError:
        raise SyntaxError("Operation must have [method]")
    try:
        expects = convert_literal(supported_op["expects"])
    except KeyError:
        raise SyntaxError("Operation must have [expects]")
    try:
        returns = convert_literal(supported_op["returns"])
    except KeyError:
        raise SyntaxError("Operation must have [returns]")
    try:
        status = supported_op["possibleStatus"]
    except KeyError:
        raise SyntaxError("Operation must have [possibleStatus]")
    # Create the HydraClassOp object
    op = HydraClassOp(name, method, expects, returns, status) # type: ignore
    return op


def create_status(possible_status: Dict[str, Any]) -> HydraStatus:
    """Create a HydraStatus object from the possibleStatus."""
    # Syntax checks
    try:
        title = possible_status["title"]
    except KeyError:
        raise SyntaxError("Status must have [title]")
    try:
        code = possible_status["statusCode"]
    except KeyError:
        raise SyntaxError("Status must have [statusCode]")
    try:
        description = convert_literal(possible_status["description"])
    except KeyError:
        raise SyntaxError("Status must have [description]")
    # Create the HydraStatus object
    status = HydraStatus(code, title, description) # type: ignore
    return status


if __name__ == "__main__":
    api_doc = create_doc(sample_document.generate())
    print(json.dumps(api_doc.generate(), indent=4, sort_keys=True))