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

    @patch('hydrus.hydraspec.doc_writer.HydraEntryPoint', spec=doc_writer.HydraEntryPoint)
    def test_context_with_entrypoint(self, mock_entry):
        """
        Test method to test if correct context is generated when HydraEntryPoint is passed

        """

        hydra_entry_point_mock = mock_entry()
        hydra_entry_point_mock.base_url = "https://hydrus.com/api"
        hydra_entry_point_mock.entrypoint = "EntryPoint"

        context = doc_writer.Context('https://hydrus.com/api',
                                     entrypoint=hydra_entry_point_mock)

        expected_context = {
            "EntryPoint": "vocab:EntryPoint",
            "vocab": "https://hydrus.com/api/vocab#"
        }
        self.assertEqual(expected_context, context.generate())

    def test_context_with_class(self):
        """
        Test method to test if correct context is generated when HydraClass is passed

        """

        mocked_hydra_class = MagicMock()
        with patch('hydrus.hydraspec.doc_writer.HydraClass', mocked_hydra_class, spec_set=doc_writer.HydraClass):
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

                context = doc_writer.Context('https://hydrus.com/api', class_=mocked_hydra_class)

                expected_context = {
                    "vocab": "https://hydrus.com/api/vocab#",
                    "hydra": "http://www.w3.org/ns/hydra/core#",
                    "members": "http://www.w3.org/ns/hydra/core#member",
                    "object": "http://schema.org/object",
                    "Pet": "vocab:Pet",
                    "id": ""
                }

                self.assertEqual(expected_context, context.generate())

    if __name__ == '__main__':
        unittest.main()
