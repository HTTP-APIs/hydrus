import unittest
from hydrus.hydraspec import doc_writer


class TestDocWriter(unittest.TestCase):
    
    # test context class methods
    def test_context_with_nothing(self):
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
        self.assertEqual(expected_context,context.generate())


    if __name__ == '__main__':
    
        unittest.main()
