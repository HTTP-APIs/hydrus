"""Sample to create Hydra APIDocumentation using doc_writer."""

from hydra_python_core.doc_writer import (HydraDoc, HydraClass, HydraClassProp, HydraClassOp,
                                          HydraStatus, HydraError)
from typing import Any, Dict, Union

# Creating the HydraDoc object, this is the primary class for the Doc
API_NAME = "api"                # Name of the API, will serve as EntryPoint
BASE_URL = "https://hydrus.com/"    # The base url at which the API is hosted
# NOTE: The API will be accessible at BASE_URL + ENTRY_POINT
# (http://hydrus.com/api/)

# Create ApiDoc Object
api_doc = HydraDoc(API_NAME,
                   "Title for the API Documentation",
                   "Description for the API Documentation",
                   API_NAME,
                   BASE_URL)


# Creating classes for the API
class_uri = "dummyClass"      # URI of class for the HydraClass
class_title = "dummyClass"                      # Title of the Class
class_description = "A dummyClass for demo"     # Description of the class
class_ = HydraClass(class_uri, class_title, class_description, endpoint=False)

# Class with single instance
class_2_uri = "singleClass"
class_2_title = "singleClass"
class_2_description = "A non collection class"
class_2 = HydraClass(class_2_uri, class_2_title,
                     class_2_description, endpoint=True)

# Another class with single instance, will be used as nested class

class_1_uri = "anotherSingleClass"
class_1_title = "anotherSingleClass"
class_1_description = "An another non collection class"
class_1 = HydraClass(class_1_uri, class_1_title,
                     class_1_description, endpoint=True)

# Class not having any methods except put and get
class_3_uri = "extraClass"
class_3_title = "extraClass"
class_3_description = "Class without any explicit methods"
class_3 = HydraClass(class_3_uri, class_3_title,
                     class_3_description, endpoint=False)

# NOTE: Setting endpoint=True creates an endpoint for the class itself, this is usually for classes
#       that have single instances.
#       These classes should not ideally have a Collection, although
#       Hydrus will allow creation of Collections for them


# Create new properties for the class
# The URI of the class of the property
prop1_uri = "http://props.hydrus.com/prop1"
prop1_title = "Prop1"                   # Title of the property

dummyProp1 = HydraClassProp(prop1_uri, prop1_title,
                            required=True, read=False, write=True)


prop2_uri = "http://props.hydrus.com/prop2"
prop2_title = "Prop2"

dummyProp2 = HydraClassProp(prop1_uri, prop2_title,
                            required=False, read=False, write=True)
# NOTE: Properties that are required=True must be added during class object creation
#       Properties that are read=True are read only
#       Properties that are write=True are writable


# Create operations for the class
op_name = "UpdateClass"  # The name of the operation
op_method = "POST"  # The method of the Operation [GET, POST, PUT, DELETE]
# URI of the object that is expected for the operation
op_expects = "vocab:dummyClass"
op_returns = None   # URI of the object that is returned by the operation
# List of statusCode for the operation
op_status = [HydraStatus(code=200, title="dummyClass updated.")]

op1 = HydraClassOp(op_name,
                   op_method,
                   op_expects,
                   op_returns,
                   op_status)

# Same way add DELETE, PUT and GET operations
op2_status = [HydraStatus(code=200, title="dummyClass deleted.")]
op2 = HydraClassOp("DeleteClass", "DELETE", None, None, op2_status)
op3_status = [HydraStatus(code=201, title="dummyClass successfully added.")]
op3 = HydraClassOp("AddClass", "PUT", "vocab:dummyClass", None, op3_status)
op4_status = [HydraStatus(code=200, title="dummyClass returned.")]
op4 = HydraClassOp("GetClass", "GET", None, "vocab:dummyClass", op4_status)

# Operations for non collection class
class_2_op1_status = [HydraStatus(code=200, title="singleClass changed.")]
class_2_op1 = HydraClassOp("UpdateClass", "POST",
                           "vocab:singleClass", None, class_2_op1_status)
class_2_op2_status = [HydraStatus(code=200, title="singleClass deleted.")]
class_2_op2 = HydraClassOp("DeleteClass", "DELETE",
                           None, None, class_2_op2_status)
class_2_op3_status = [HydraStatus(code=201, title="singleClass successfully added.")]
class_2_op3 = HydraClassOp(
    "AddClass", "PUT", "vocab:singleClass", None, class_2_op3_status)
class_2_op4_status = [HydraStatus(code=200, title="singleClass returned.")]
class_2_op4 = HydraClassOp("GetClass", "GET", None,
                           "vocab:singleClass", class_2_op4_status)

class_1_op1_status = [HydraStatus(code=200, title="anotherSingleClass returned.")]
class_1_op1 = HydraClassOp("GetClass", "GET", None,
                           "vocab:anotherSingleClass", class_1_op1_status)
# Add the properties to the classes
class_.add_supported_prop(dummyProp1)
class_.add_supported_prop(dummyProp2)
class_2.add_supported_prop(dummyProp1)
class_2.add_supported_prop(dummyProp2)
class_2.add_supported_prop(HydraClassProp(
    "vocab:dummyClass", "dummyProp", required=False, read=False, write=False))
class_2.add_supported_prop(HydraClassProp(
    "vocab:anotherSingleClass", "singleClassProp", required=False, read=False, write=False))
class_1.add_supported_prop(dummyProp1)
# Add the operations to the classes
class_.add_supported_op(op1)
class_.add_supported_op(op2)
class_.add_supported_op(op3)
class_.add_supported_op(op4)
class_2.add_supported_op(class_2_op1)
class_2.add_supported_op(class_2_op2)
class_2.add_supported_op(class_2_op3)
class_2.add_supported_op(class_2_op4)
class_1.add_supported_op(class_1_op1)

# Add the classes to the HydraDoc
api_doc.add_supported_class(class_, collection=True, collection_path="DcTest")
api_doc.add_supported_class(class_3, collection=True, collection_path="EcTest")
api_doc.add_supported_class(class_2, collection=False)
api_doc.add_supported_class(class_1, collection=False)
# NOTE: Using collection=True creates a HydraCollection for the class.
#       The name of the Collection is class_.title+"Collection"
#       The collection inherently supports GET and PUT operations

# Other operations needed for the Doc
api_doc.add_baseResource(
)      # Creates the base Resource Class and adds it to the API Documentation
# Creates the base Collection Class and adds it to the API Documentation
api_doc.add_baseCollection()
# Generates the EntryPoint object for the Doc using the Classes and Collections
api_doc.gen_EntryPoint()


# Generate the complete API Documentation
doc = api_doc.generate(
)  # type: Union[Dict[str, Any], str]       # Returns the entire API Documentation as a Python dict

if __name__ == "__main__":
    """Print the complete sample Doc in doc_writer_sample_output.py."""
    import json

    dump = json.dumps(doc, indent=4, sort_keys=True)
    doc = '''"""Generated API Documentation sample using doc_writer_sample.py."""
    \ndoc = {}\n'''.format(dump)
    # Python does not recognise null, true and false in JSON format, convert
    # them to string
    doc = doc.replace('true', '"true"')
    doc = doc.replace('false', '"false"')
    doc = doc.replace('null', '"null"')
    with open("doc_writer_sample_output.py", "w") as f:
        f.write(doc)
