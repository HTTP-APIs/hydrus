import unittest
from hydrus.hydraspec import doc_writer
import unittest.mock as mock


class TestDocWriter(unittest.TestCase):
    hydra_entry_point_mock = mock.Mock(spec_set=doc_writer.HydraEntryPoint)
    hydra_class_mock = mock.Mock(spec=doc_writer.HydraClass)
    hydra_prop1 = mock.Mock(spec=doc_writer.HydraClassProp)

    # test context class methods
    def test_context_with_nothing(self):
        """


        :return:
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

    def test_context_with_entrypoint(self):
        """

        :return:
        """
        context = doc_writer.Context('https://hydrus.com/api',
                                     entrypoint=self.hydra_entry_point_mock("https://hydrus.com/api", "EntryPoint"))

        expected_context = {
            "EntryPoint": "vocab:EntryPoint",
            "vocab": "https://hydrus.com/api/vocab#"
        }
        self.assertEqual(expected_context, context.generate())

    def test_context_with_class(self):
        self.hydra_class_mock.id_ = "vocab:Pet"
        self.hydra_class_mock.title = "Pet"
        self.hydra_class_mock.desc = "Pet"
        self.hydra_prop1.prop = ""
        self.hydra_prop1.readonly = "true"
        self.hydra_prop1.required = "false"
        self.hydra_prop1.title = "id"
        self.hydra_prop1.writeonly = "true"
        self.hydra_class_mock.supportedProperty = [self.hydra_prop1]

        context = doc_writer.Context('https://hydrus.com/api', class_=self.hydra_class_mock)

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
