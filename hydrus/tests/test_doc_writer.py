import unittest
from hydrus.hydraspec import doc_writer
from unittest.mock import MagicMock, patch


class TestDocWriter(unittest.TestCase):

    # test context class methods
    def test_context_with_nothing(self):
        """
        Test method to test if correct context is generated when no arguments are passed

        """
        context = doc_writer.Context('https://hydrus.com/api')
        expected_context = {
            "hydra": "http://www.w3.org/ns/hydra/core#",
            "property": {
                "@type": "@id",
                "@id": "hydra:property"
            },
            "supportedClass": "hydra:supportedClass",
            "supportedProperty": "hydra:supportedProperty",
            "supportedOperation": "hydra:supportedOperation",
            "statusCodes": "hydra:statusCodes",
            "label": "rdfs:label",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "vocab": "https://hydrus.com/api/vocab#",
            # "vocab": "localhost/api/vocab#",
            "domain": {
                "@type": "@id",
                "@id": "rdfs:domain"
            },
            "ApiDocumentation": "hydra:ApiDocumentation",
            "range": {
                "@type": "@id",
                "@id": "rdfs:range"
            },
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "title": "hydra:title",
            "expects": {
                "@type": "@id",
                "@id": "hydra:expects"
            },
            "returns": {
                "@id": "hydra:returns",
                "@type": "@id"
            },
            "readonly": "hydra:readonly",
            "writeonly": "hydra:writeonly",
            "possibleStatus": "hydra:possibleStatus",
            "required": "hydra:required",
            "method": "hydra:method",
            "statusCode": "hydra:statusCode",
            "description": "hydra:description",
            "subClassOf": {
                "@id": "rdfs:subClassOf",
                "@type": "@id"
            }
        }
        self.assertEqual(expected_context, context.generate())

    @patch('hydrus.hydraspec.doc_writer.HydraEntryPoint',
           spec=doc_writer.HydraEntryPoint)
    def test_context_with_entrypoint(self, mock_entry):
        """
        Test method to test if correct context is generated when HydraEntryPoint is passed

        """

        hydra_entry_point_mock = mock_entry()
        hydra_entry_point_mock.base_url = "http://petstore.swagger.io/v2"
        hydra_entry_point_mock.entrypoint = "EntryPoint"

        context = doc_writer.Context('http://petstore.swagger.io/v2',
                                     entrypoint=hydra_entry_point_mock)

        expected_context = {
            "EntryPoint": "vocab:EntryPoint",
            "vocab": "http://petstore.swagger.io/v2/vocab#"
        }
        self.assertEqual(expected_context, context.generate())

    def test_context_with_class(self):
        """
        Test method to test if correct context is generated when HydraClass is passed

        """

        mocked_hydra_class = MagicMock()
        with patch(
                'hydrus.hydraspec.doc_writer.HydraClass',
                mocked_hydra_class, spec_set=doc_writer.HydraClass):
            mocked_hydra_property = MagicMock()
            mocked_hydra_class.id_ = "vocab:Pet"
            mocked_hydra_class.title = "Pet"
            mocked_hydra_class.desc = "Pet"
            with patch('hydrus.hydraspec.doc_writer.HydraClassProp', mocked_hydra_property,
                       spec_set=doc_writer.HydraClassProp):
                mocked_hydra_property.prop = ""
                mocked_hydra_property.readonly = "true"
                mocked_hydra_property.required = "false"
                mocked_hydra_property.title = "id"
                mocked_hydra_property.writeonly = "true"

                mocked_hydra_class.supportedProperty = [mocked_hydra_property]

                context = doc_writer.Context(
                    'http://petstore.swagger.io/v2',
                    class_=mocked_hydra_class)

                expected_context = {
                    "vocab": "http://petstore.swagger.io/v2/vocab#",
                    "hydra": "http://www.w3.org/ns/hydra/core#",
                    "members": "http://www.w3.org/ns/hydra/core#member",
                    "object": "http://schema.org/object",
                    "Pet": "vocab:Pet",
                    "id": ""
                }

                self.assertEqual(expected_context, context.generate())

    @patch('hydrus.hydraspec.doc_writer.HydraClass', spec=doc_writer.HydraClass)
    @patch('hydrus.hydraspec.doc_writer.HydraCollection',
           spec=doc_writer.HydraCollection)
    def test_context_with_collection(self, hydra_class, hydra_collection):
        """
        Test method to test if correct context is generated when HydraCollection is passed

        """
        mocked_hydra_class = hydra_class()
        mocked_hydra_class.id_ = "vocab:Pet"
        mocked_hydra_class.title = "Pet"
        mocked_hydra_class.desc = "Pet"

        mocked_hydra_collection = hydra_collection()
        mocked_hydra_collection.class_ = mocked_hydra_class
        mocked_hydra_collection.name = "{}Collection".format(mocked_hydra_class.title)
        context = doc_writer.Context(
            'http://petstore.swagger.io/v2',
            collection=mocked_hydra_collection)
        expected_context = {
            "vocab": "http://petstore.swagger.io/v2/vocab#",
            "hydra": "http://www.w3.org/ns/hydra/core#",
            "members": "http://www.w3.org/ns/hydra/core#member",
            "PetCollection": "vocab:PetCollection",
            "Pet": "vocab:Pet"
        }

        self.assertEqual(expected_context, context.generate())

    if __name__ == '__main__':
        unittest.main()
