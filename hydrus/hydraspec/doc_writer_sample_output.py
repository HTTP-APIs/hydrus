"""Generated API Documentation sample using doc_writer_sample.py."""

doc = {
    "@context": {
        "ApiDocumentation": "hydra:ApiDocumentation",
        "description": "hydra:description",
        "domain": {
            "@id": "rdfs:domain",
            "@type": "@id"
        },
        "expects": {
            "@id": "hydra:expects",
            "@type": "@id"
        },
        "hydra": "http://www.w3.org/ns/hydra/core#",
        "label": "rdfs:label",
        "method": "hydra:method",
        "possibleStatus": "hydra:possibleStatus",
        "property": {
            "@id": "hydra:property",
            "@type": "@id"
        },
        "range": {
            "@id": "rdfs:range",
            "@type": "@id"
        },
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "readonly": "hydra:readonly",
        "required": "hydra:required",
        "returns": {
            "@id": "hydra:returns",
            "@type": "@id"
        },
        "statusCode": "hydra:statusCode",
        "statusCodes": "hydra:statusCodes",
        "subClassOf": {
            "@id": "rdfs:subClassOf",
            "@type": "@id"
        },
        "supportedClass": "hydra:supportedClass",
        "supportedOperation": "hydra:supportedOperation",
        "supportedProperty": "hydra:supportedProperty",
        "title": "hydra:title",
        "vocab": "https://hydrus.com/demoapi/vocab#",
        "writeonly": "hydra:writeonly"
    },
    "@id": "https://hydrus.com/demoapi/vocab",
    "@type": "ApiDocumentation",
    "description": "Description for the API Documentation",
    "possibleStatus": [],
    "supportedClass": [
        {
            "@id": "http://hydrus.com/dummyClass",
            "@type": "hydra:Class",
            "description": "A dummyClass for demo",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "vocab:Drone",
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "description": "Drone updated",
                            "statusCode": 200
                        }
                    ],
                    "returns": "null",
                    "title": "SubmitProp"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://hydrus.com/prop1",
                    "readonly": "false",
                    "required": "false",
                    "title": "Prop1",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://hydrus.com/prop1",
                    "readonly": "false",
                    "required": "false",
                    "title": "Prop2",
                    "writeonly": "true"
                }
            ],
            "title": "dummyClass"
        },
        {
            "@id": "http://www.w3.org/ns/hydra/core#Resource",
            "@type": "hydra:Class",
            "description": "null",
            "supportedOperation": [],
            "supportedProperty": [],
            "title": "Resource"
        },
        {
            "@id": "http://www.w3.org/ns/hydra/core#Collection",
            "@type": "hydra:Class",
            "description": "null",
            "supportedOperation": [],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "null",
                    "title": "members",
                    "writeonly": "false"
                }
            ],
            "title": "Collection"
        },
        {
            "@id": "vocab:dummyClassCollection",
            "@type": "hydra:Class",
            "description": "A collection of dummyclass",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:dummyclass_collection_retrieve",
                    "@type": "hydra:Operation",
                    "description": "Retrieves all dummyClass entities",
                    "expects": "null",
                    "method": "GET",
                    "returns": "vocab:dummyClassCollection",
                    "statusCodes": []
                },
                {
                    "@id": "_:dummyclass_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new dummyClass entitity",
                    "expects": "http://hydrus.com/dummyClass",
                    "method": "PUT",
                    "returns": "http://hydrus.com/dummyClass",
                    "statusCodes": [
                        {
                            "description": "If the dummyClass entity was created successfully.",
                            "statusCode": 201
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The dummyclass",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "false",
                    "title": "members",
                    "writeonly": "false"
                }
            ],
            "title": "dummyClassCollection"
        },
        {
            "@id": "vocab:EntryPoint",
            "@type": "hydra:Class",
            "description": "The main entry point or homepage of the API.",
            "supportedOperation": [
                {
                    "@id": "_:entry_point",
                    "@type": "hydra:Operation",
                    "description": "The APIs main entry point.",
                    "expects": "null",
                    "method": "GET",
                    "returns": "null",
                    "statusCodes": "vocab:EntryPoint"
                }
            ],
            "supportedProperty": [
                {
                    "hydra:description": "The dummyClassCollection collection",
                    "hydra:title": "dummyclasscollection",
                    "property": {
                        "@id": "vocab:EntryPoint/dummyClassCollection",
                        "@type": "hydra:Link",
                        "description": "The dummyClassCollection collection",
                        "domain": "vocab:EntryPoint",
                        "label": "dummyClassCollection",
                        "range": "vocab:dummyClassCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:_:dummyclass_collection_retrieve",
                                "@type": "hydra:Operation",
                                "description": "Retrieves all dummyClass entities",
                                "expects": "null",
                                "method": "GET",
                                "returns": "vocab:dummyClassCollection",
                                "statusCodes": []
                            },
                            {
                                "@id": "_:_:dummyclass_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new dummyClass entitity",
                                "expects": "http://hydrus.com/dummyClass",
                                "method": "PUT",
                                "returns": "http://hydrus.com/dummyClass",
                                "statusCodes": [
                                    {
                                        "description": "If the dummyClass entity was created successfully.",
                                        "statusCode": 201
                                    }
                                ]
                            }
                        ]
                    },
                    "readonly": "true",
                    "required": "null",
                    "writeonly": "false"
                }
            ],
            "title": "EntryPoint"
        }
    ],
    "title": "Title for the API Documentation"
}