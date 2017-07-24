"""Sample to create Hydra APIDocumentation using doc_writer."""

from hydrus.hydraspec.doc_writer import HydraDoc, HydraClass, HydraClassProp, HydraClassOp

"""Creating the HydraDoc object, this is the primary class for the Doc"""
API_NAME = "demoapi"                # Name of the API
BASE_URL = "https://hydrus.com/"    # The base url at which the API is hosted
ENTRY_POINT = "api"                 # The entrypoint where the API will  be accessed
# NOTE: The API will be accessible at BASE_URL + ENTRY_POINT (http://hydrus.com/api/)

api_doc = HydraDoc(API_NAME,
                   "Title for the API Documentation",
                   "Description for the API Documentation",
                   ENTRY_POINT,
                   BASE_URL)


"""Creating classes for the API"""
class_uri = "http://hydrus.com/dummyClass"      # URI of class for the HydraClass
class_title = "dummyClass"                      # Title of the Class
class_description = "A dummyClass for demo"     # Description of the class

class_ = HydraClass(class_uri, class_title, class_description, endpoint=False)
# NOTE: Setting endpoint=True creates an endpoint for the class itself, this is usually for classes that have single instances.
#       These classes should not ideally have a Collection, although Hydrus will allow creation of Collections for them


"""Create new properties for the class"""
prop1_uri = "http://hydrus.com/prop1"   # The URI of the class of the property
prop1_title = "Prop1"                   # Title of the property

dummyProp1 = HydraClassProp(prop1_uri, prop1_title, required=False, read=False, write=True)


prop2_uri = "http://hydrus.com/prop2"
prop2_title = "Prop2"

dummyProp2 = HydraClassProp(prop1_uri, prop2_title, required=False, read=False, write=True)
# NOTE: Properties that are required=True must be added during class object creation
#       Properties that are read=True are read only
#       Properties that are write=True are writable


"""Create operations for the class"""
op_name = "SubmitProp"          # The name of the operation
op_method = "POST"              # The method of the Operation [GET, POST, PUT, DELETE]
op_expects = "vocab:Drone"      # URI of the object that is expected for the operation
op_returns = None               # URI of the object that is returned by the operation
op_status = [{"statusCode": 200, "description": "Drone updated"}]   # List of statusCode for the operation

op1 = HydraClassOp(op_name,
                   op_method,
                   op_expects,
                   op_returns,
                   op_status)


"""Add the operation to the Class"""
class_.add_supported_prop(dummyProp1)
class_.add_supported_prop(dummyProp2)

"""Add the properties to the Class"""
class_.add_supported_op(op1)


"""Add the classes to the HydraDoc"""
api_doc.add_supported_class(class_, collection=True)
# NOTE: Using collection=True creates a HydraCollection for the class.
#       The name of the Collection is class_.title+"Collection"
#       The collection inherently supports GET and PUT operations

"""Other operations needed for the Doc"""
api_doc.add_baseResource()      # Creates the base Resource Class and adds it to the API Documentation
api_doc.add_baseCollection()    # Creates the base Collection Class and adds it to the API Documentation
api_doc.gen_EntryPoint()        # Generates the EntryPoint object for the Doc using the Classes and Collections


"""Generate the complete API Documentation"""
doc = api_doc.generate()        # Returns the entire API Documentation as a Python dict

if __name__ == "__main__":
    """Print the complete sample Doc in doc_writer_sample_output.py."""
    import json

    dump = json.dumps(doc, indent=4, sort_keys=True)
    doc = '''"""Generated API Documentation sample using doc_writer_sample.py."""\n\ndoc = %s''' % dump
    # Python does not recognise null, true and false in JSON format, convert them to string
    doc = doc.replace('true', '"true"')
    doc = doc.replace('false', '"false"')
    doc = doc.replace('null', '"null"')
    f = open("doc_writer_sample_output.py", "w")
    f.write(doc)
    f.close()
