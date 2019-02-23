import unittest
import os
import hydrus

from hydrus.hydraspec.doc_writer import HydraClass
from hydrus.parser import openapi_parser
import yaml


def import_doc():
    print("Importing Open Api Documentation ..")
    abs_path = os.path.abspath("{}/samples/petstore_openapi.yaml".format(os.path.dirname(
        hydrus.__file__)))
    with open(abs_path, 'r') as stream:
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
        """Test if the empty object is being generated correctly """
        object_ = openapi_parser.generate_empty_object()
        assert isinstance(object_["prop_definition"], list)
        assert isinstance(object_["op_definition"], list)
        assert isinstance(object_["class_definition"], type)
        assert isinstance(object_["collection"], bool)

    def test_valid_endpoint(self):
        """Test if the endpoint is valid and can be parsed """
        path = 'A/B/{id}/C/D'
        result = openapi_parser.valid_endpoint(path)
        assert result is "False"
        assert isinstance(result, str)
        path = 'A/B/{id}'
        result = openapi_parser.valid_endpoint(path)
        assert result is "Collection"
        assert isinstance(result, str)
        path = 'A/B/id'
        result = openapi_parser.valid_endpoint(path)
        assert result is "True"
        assert isinstance(result, str)

    def test_get_class_name(self):
        """Test if the class name is being extracted properly from the path """
        path = "A/B/C/Pet"
        path_list = path.split('/')
        result = openapi_parser.get_class_name(path_list)
        assert result is path_list[3]
        assert isinstance(result, str)

    def test_get_data_from_location(self):
        """Test if the data from the location given is being fetched correctly"""
        path = '#/definitions/Order'
        path_list = path.split('/')
        result = openapi_parser.get_data_at_location(path_list, self.doc)
        response = self.doc["definitions"]["Order"]
        assert response is result

    def test_sanitise_path(self):
        """Test if the variables can be removed from the path"""
        path = "A/B/C/{id}"
        result = openapi_parser.sanitise_path(path)
        assert isinstance(result, str)

    def test_allow_parameter(self):
        """Test if the rules are being followed """
        parameter_block = self.doc["paths"]["/pet"]["post"]["parameters"][0]
        result = openapi_parser.allow_parameter(parameter_block)
        assert result is True
        assert isinstance(result, bool)
        parameter_block = self.doc["paths"]["/pet"]["get"]["parameters"][0]
        result = openapi_parser.allow_parameter(parameter_block)
        assert result is False
        assert isinstance(result, bool)

    def test_parse(self):
        """Test the hydra documentation """
        result = openapi_parser.parse(self.doc)
        assert isinstance(result, dict)

    def test_check_collection(self):
        """Test if collections are being identified properly"""
        schema_block = {
            'type': 'array', 'items': {
                '$ref': '#/definitions/Pet'}}
        method = "/Pet"
        result = openapi_parser.check_collection(schema_block, method)
        assert isinstance(result, bool)
        assert result

    def test_check_collection_false(self):
        "Test if non collections are identified"
        schema = {'$ref': '#/definitions/User'}
        method = "/Pet"
        result = openapi_parser.check_collection(schema, method)
        assert isinstance(result, bool)
        assert not result


if __name__ == '__main__':
    print("Starting tests ..")
    unittest.main()
