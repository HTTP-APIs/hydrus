import unittest

from hydrus.hydraspec.doc_writer import HydraClass
from hydrus.parser import openapi_parser
import yaml


def import_doc():
    print("Importing Open Api Documentation ..")
    with open("../samples/petstore_openapi.yaml", 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


class TestParser(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        doc = import_doc()
        self.doc = doc

    @classmethod
    def tearDownClass(cls):
        pass

    def test_generate_empty_object(self):
        object_ = openapi_parser.generate_empty_object()
        assert type(object_["prop_definition"]) is list
        assert type(object_["op_definition"]) is list
        assert type(object_["class_definition"]) is type
        assert type(object_["collection"]) is bool

    def test_valid_endpoint(self):
        path = 'A/B/{id}/C/D'
        result = openapi_parser.valid_endpoint(path)
        assert result is "False"
        assert type(result) is str
        path = 'A/B/{id}'
        result = openapi_parser.valid_endpoint(path)
        assert result is "Collection"
        assert type(result) is str
        path = 'A/B/id'
        result = openapi_parser.valid_endpoint(path)
        assert result is "True"
        assert type(result) is str
    def test_get_class_name(self):
        path = "A/B/C/Pet"
        path_list = path.split('/')
        result = openapi_parser.get_class_name(path_list)
        assert result is path_list[3]
        assert type(result) is str
    def test_get_data_from_location(self):
        path = '#/definitions/Order'
        path_list = path.split('/')
        result = openapi_parser.get_data_at_location(path_list,self.doc)
        response = self.doc["definitions"]["Order"]
        assert response is result
    def test_sanitise_path(self):
        path = "A/B/C/{id}"
        result = openapi_parser.sanitise_path(path)
        assert result == 'A/B/C'
        assert type(result) is str
    def test_allow_parameter(self):
        parameter_block = self.doc["paths"]["/pet"]["post"]["parameters"][0]
        result = openapi_parser.allow_parameter(parameter_block)
        assert result is True
        assert type(result) is bool




if __name__ == '__main__':
    print("Starting tests ..")
    unittest.main()
