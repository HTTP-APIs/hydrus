'''Contsructor to take a Python dict containing an API Documentation and
create a HydraDoc object for it'''
import re
import json
from hydrus.hydraspec.doc_writer_sample import api_doc as sample_document
from hydrus.hydraspec.doc_writer import HydraDoc, HydraClass, HydraClassProp, HydraClassOp
from hydrus.hydraspec.doc_writer import HydraStatus

def error_mapping(body):
    """Function returns starting error message based on its body type."""
    error_map = {
        "doc" : "The API Documentation must have",
        "class_dict" : "Class must have",
        "supported_prop" : "Property must have",
        "supported_op": "Operation must have",
        "possible_status": "Status must have"
    }
    return error_map[body]

def input_key_check(body, key, body_type, literal):
    """Function to validate key inside the dictonary payload"""
    try:
        if literal:
            return convert_literal(body[key])
        return body[key]
    except KeyError:
        raise SyntaxError("{0} [{1}]".format(error_mapping(body_type), key))

def create_doc(doc, HYDRUS_SERVER_URL=None, API_NAME=None):
    """Create the HydraDoc object from the API Documentation."""
    # Check @id
    try:
        id_ = doc["@id"]
    except KeyError:
        raise SyntaxError("The API Documentation must have [@id]")

    # Extract base_url, entrypoint and API name
    match_obj = re.match(r'(.*)://(.*)/(.*)/vocab#?', id_, re.M | re.I)
    if match_obj:
        base_url = match_obj.group(1) + '://' + match_obj.group(2) + '/'
        entrypoint = match_obj.group(3)

    # Syntax checks
    else:
        raise SyntaxError("The '@id' of the Documentation must be of the form:\n'[protocol] :// [base url] / [entrypoint] / vocab'")
    doc_keys = {
        "description" : False,
        "title" : False,
        "supportedClass" : False,
        "@context" : False,
        "possibleStatus" : False
    }
    result = {}
    for k, literal in doc_keys.items():
        result[k] = input_key_check(doc, k, "doc", literal)

    # EntryPoint object
    entrypoint_obj = get_entrypoint(doc)     # getEntrypoint checks if all classes have @id

    # Main doc object
    if HYDRUS_SERVER_URL is not None and API_NAME is not None:
        apidoc = HydraDoc(API_NAME, result["title"], result["description"], API_NAME, HYDRUS_SERVER_URL)
    else:
        apidoc = HydraDoc(entrypoint, result["title"], result["description"], entrypoint, base_url)

    # additional context entries
    for entry in result["@context"]:
        apidoc.add_to_context(entry, result["@context"][entry])

    # add all parsed_classes
    for class_ in result["supportedClass"]:
        class_obj, collection = create_class(entrypoint_obj, class_)
        if class_obj:
            apidoc.add_supported_class(class_obj, collection=collection)

    # add possibleStatus
    for status in result["possibleStatus"]:
        status_obj = create_status(status)
        apidoc.add_possible_status(status_obj)

    apidoc.add_baseResource()
    apidoc.add_baseCollection()
    apidoc.gen_EntryPoint()
    return apidoc


def create_class(entrypoint, class_dict):
    """Create HydraClass objects for classes in the API Documentation."""
    # Base classes not used
    exclude_list = ['http://www.w3.org/ns/hydra/core#Resource',
                    'http://www.w3.org/ns/hydra/core#Collection',
                    entrypoint["@id"]]
    id_ = class_dict["@id"]
    if id_ in exclude_list:
        return None, None
    match_obj = re.match(r'vocab:(.*)', id_, re.M | re.I)
    if match_obj:
        id_ = match_obj.group(1)

    doc_keys = {
        "supportedProperty" : False,
        "title" : False,
        "description" : False,
        "supportedOperation" : False
    }

    result = {}
    for k, literal in doc_keys.items():
        result[k] = input_key_check(class_dict, k, "class_dict", literal)

    # See if class_dict is a Collection Class
    collection = re.match(r'(.*)Collection(.*)', result["title"], re.M | re.I)
    if collection:
        return None, None

    # Check if class has it's own endpoint
    endpoint = class_in_endpoint(class_dict, entrypoint)

    # Check if class has a Collection
    collection = collection_in_endpoint(class_dict, entrypoint)

    # Create the HydraClass object
    class_ = HydraClass(id_, result["title"], result["description"], endpoint=endpoint)

    # Add supportedProperty for the Class
    for prop in result["supportedProperty"]:
        prop_obj = create_property(prop)
        class_.add_supported_prop(prop_obj)

    # Add supportedOperation for the Class
    for op_ in result["supportedOperation"]:
        op_obj = create_operation(op_)
        class_.add_supported_op(op_obj)

    return class_, collection


def get_entrypoint(doc):
    """Find and return the entrypoint object in the doc."""
    # Search supportedClass
    for class_ in doc["supportedClass"]:
        # Check the @id for each class
        try:
            class_id = class_["@id"]
        except KeyError:
            raise SyntaxError("Each supportedClass must have [@id]")
        # Match with regular expression
        match_obj = re.match(r'vocab:(.*)EntryPoint', class_id)
        # Return the entrypoint object
        if match_obj:
            return class_
    # If not found, raise error
    raise SyntaxError("No EntryPoint class found")


def convert_literal(literal):
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
        return literal
    elif isinstance(literal, (bool,)) or literal is None:
        return literal
    else:
        # Raise error for non string objects
        raise TypeError("Literal not recognised")


def create_property(supported_prop):
    """Create a HydraClassProp object from the supportedProperty."""
    # Syntax checks

    doc_keys = {
        "property" : False,
        "title": False,
        "readonly": True,
        "writeonly": True,
        "required": True
    }
    result = {}
    for k, literal in doc_keys.items():
        result[k] = input_key_check(supported_prop, k, "supported_prop", literal)
    # Create the HydraClassProp object
    prop = HydraClassProp(result["property"], result["title"], required=result["required"], read=result["readonly"], write=result["writeonly"])
    return prop

def class_in_endpoint(class_, entrypoint):
    """Check if a given class is in the EntryPoint object as a class."""
    regex = r'(vocab:)?(.*)EntryPoint/(.*/)?' + re.escape(class_["title"]) + r'$'
    # Check supportedProperty for the EntryPoint
    try:
        supported_property = entrypoint["supportedProperty"]
    except KeyError:
        raise SyntaxError("EntryPoint must have [supportedProperty]")

    # Check all endpoints in supportedProperty
    for prop in supported_property:
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
        match_obj = re.match(regex, id_)
        if match_obj:
            return True
    return False


def collection_in_endpoint(class_, entrypoint):
    """Check if a given class is in the EntryPoint object as a collection."""
    regex = r'(vocab:)?(.*)EntryPoint/(.*/)?' + class_["title"] + "Collection"
    # Check supportedProperty for the EntryPoint
    try:
        supported_property = entrypoint["supportedProperty"]
    except KeyError:
        raise SyntaxError("EntryPoint must have [supportedProperty]")

    # Check all endpoints in supportedProperty
    for prop in supported_property:
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
        match_obj = re.match(regex, id_)
        if match_obj:
            return True
    return False


def create_operation(supported_op):
    """Create a HyraClassOp object from the supportedOperation."""
    # Syntax checks
    doc_keys = {
        "title": False,
        "method" : False,
        "expects": True,
        "returns": True,
        "possibleStatus": False
    }
    result = {}
    for k, literal in doc_keys.items():
        result[k] = input_key_check(supported_op, k, "supported_op", literal)

    # Create the HydraClassOp object
    op_ = HydraClassOp(result["title"], result["method"], result["expects"], result["returns"], result["possibleStatus"])
    return op_


def create_status(possible_status):
    """Create a HydraStatus object from the possibleStatus."""
    # Syntax checks
    doc_keys = {
        "title": False,
        "statusCode": False,
        "description": True
    }
    result = {}
    for k, literal in doc_keys.items():
        result[k] = input_key_check(possible_status, k, "possible_status", literal)
    # Create the HydraStatus object
    status = HydraStatus(result["statusCode"], result["title"], result["description"])
    return status


if __name__ == "__main__":
    api_doc = create_doc(sample_document.generate())
    print(json.dumps(api_doc.generate(), indent=4, sort_keys=True))
