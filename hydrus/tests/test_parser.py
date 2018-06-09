import unittest
from hydrus.parser import openapi_parser as parser
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
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_check_if_collection(self):
        pass


if __name__ == '__main__':
    print("Starting tests ..")
    unittest.main()