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
        "expectsHeader": "hydra:expectsHeader",
        "hydra": "http://www.w3.org/ns/hydra/core#",
        "label": "rdfs:label",
        "manages": "hydra:manages",
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
        "readable": "hydra:readable",
        "required": "hydra:required",
        "returns": {
            "@id": "hydra:returns",
            "@type": "@id"
        },
        "returnsHeader": "hydra:returnsHeader",
        "statusCode": "hydra:statusCode",
        "subClassOf": {
            "@id": "rdfs:subClassOf",
            "@type": "@id"
        },
        "supportedClass": "hydra:supportedClass",
        "supportedOperation": "hydra:supportedOperation",
        "supportedProperty": "hydra:supportedProperty",
        "title": "hydra:title",
        "vocab": "https://hydrus.com/api/vocab#",
        "writeable": "hydra:writeable"
    },
    "@id": "https://hydrus.com/api/vocab",
    "@type": "ApiDocumentation",
    "description": "Description for the API Documentation",
    "possibleStatus": [],
    "supportedClass": [
        {
            "@id": "vocab:extraClass",
            "@type": "hydra:Class",
            "description": "Class without any explicit methods",
            "supportedOperation": [],
            "supportedProperty": [],
            "title": "extraClass"
        },
        {
            "@id": "vocab:anotherSingleClass",
            "@type": "hydra:Class",
            "description": "An another non collection class",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/FindAction",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "",
                            "statusCode": 200,
                            "title": "anotherSingleClass returned."
                        }
                    ],
                    "returns": "vocab:anotherSingleClass",
                    "returnsHeader": [],
                    "title": "GetClass"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://props.hydrus.com/prop1",
                    "readable": "false",
                    "required": "true",
                    "title": "Prop1",
                    "writeable": "true"
                }
            ],
            "title": "anotherSingleClass"
        },
        {
            "@id": "vocab:singleClass",
            "@type": "hydra:Class",
            "description": "A non collection class",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "vocab:singleClass",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "",
                            "statusCode": 200,
                            "title": "singleClass changed."
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [],
                    "title": "UpdateClass"
                },
                {
                    "@type": "http://schema.org/DeleteAction",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "",
                            "statusCode": 200,
                            "title": "singleClass deleted."
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [],
                    "title": "DeleteClass"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:singleClass",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "",
                            "statusCode": 201,
                            "title": "singleClass successfully added."
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [],
                    "title": "AddClass"
                },
                {
                    "@type": "http://schema.org/FindAction",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "",
                            "statusCode": 200,
                            "title": "singleClass returned."
                        }
                    ],
                    "returns": "vocab:singleClass",
                    "returnsHeader": [],
                    "title": "GetClass"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://props.hydrus.com/prop1",
                    "readable": "false",
                    "required": "true",
                    "title": "Prop1",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://props.hydrus.com/prop1",
                    "readable": "true",
                    "required": "false",
                    "title": "Prop2",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": {
                        "@id": "vocab:singleClass/dummyProp",
                        "@type": "hydra:Link",
                        "description": "",
                        "domain": "vocab:singleClass",
                        "range": "vocab:dummyClass",
                        "supportedOperation": [],
                        "title": "dummyProp"
                    },
                    "readable": "true",
                    "required": "false",
                    "title": "dummyProp",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:anotherSingleClass",
                    "readable": "true",
                    "required": "false",
                    "title": "singleClassProp",
                    "writeable": "true"
                }
            ],
            "title": "singleClass"
        },
        {
            "@id": "vocab:dummyClass",
            "@type": "hydra:Class",
            "description": "A dummyClass for demo",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "vocab:dummyClass",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "",
                            "statusCode": 200,
                            "title": "dummyClass updated."
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [
                        "Content-Type",
                        "Content-Length"
                    ],
                    "title": "UpdateClass"
                },
                {
                    "@type": "http://schema.org/DeleteAction",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "",
                            "statusCode": 200,
                            "title": "dummyClass deleted."
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [],
                    "title": "DeleteClass"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:dummyClass",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "",
                            "statusCode": 201,
                            "title": "dummyClass successfully added."
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [],
                    "title": "AddClass"
                },
                {
                    "@type": "http://schema.org/FindAction",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "",
                            "statusCode": 200,
                            "title": "dummyClass returned."
                        }
                    ],
                    "returns": "vocab:dummyClass",
                    "returnsHeader": [],
                    "title": "GetClass"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://props.hydrus.com/prop1",
                    "readable": "false",
                    "required": "true",
                    "title": "Prop1",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://props.hydrus.com/prop1",
                    "readable": "true",
                    "required": "false",
                    "title": "Prop2",
                    "writeable": "false"
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
                    "readable": "false",
                    "required": "null",
                    "title": "members",
                    "writeable": "false"
                }
            ],
            "title": "Collection"
        },
        {
            "@id": "vocab:extraClassCollection",
            "@type": "hydra:Class",
            "description": "A collection of extraclass",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:extraclass_collection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all extraClass entities",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "vocab:extraClassCollection",
                    "returnsHeader": []
                },
                {
                    "@id": "_:extraclass_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new extraClass entity",
                    "expects": "vocab:extraClass",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "If the extraClass entity was createdsuccessfully.",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "vocab:extraClass",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The extraclass",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "false",
                    "required": "false",
                    "title": "members",
                    "writeable": "false"
                }
            ],
            "title": "extraClassCollection"
        },
        {
            "@id": "vocab:dummyClassCollection",
            "@type": "hydra:Class",
            "description": "A collection of dummyclass",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:dummyclass_collection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all dummyClass entities",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "vocab:dummyClassCollection",
                    "returnsHeader": []
                },
                {
                    "@id": "_:dummyclass_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new dummyClass entity",
                    "expects": "vocab:dummyClass",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "If the dummyClass entity was createdsuccessfully.",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "vocab:dummyClass",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The dummyclass",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "false",
                    "required": "false",
                    "title": "members",
                    "writeable": "false"
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
                    "@type": "vocab:EntryPoint",
                    "description": "The APIs main entry point.",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "null",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "hydra:description": "The anotherSingleClass Class",
                    "hydra:title": "anothersingleclass",
                    "property": {
                        "@id": "vocab:EntryPoint/anotherSingleClass",
                        "@type": "hydra:Link",
                        "description": "An another non collection class",
                        "domain": "vocab:EntryPoint",
                        "label": "anotherSingleClass",
                        "range": "vocab:anotherSingleClass",
                        "supportedOperation": [
                            {
                                "@id": "getclass",
                                "@type": "http://schema.org/FindAction",
                                "description": "null",
                                "expects": "null",
                                "expectsHeader": [],
                                "label": "GetClass",
                                "method": "GET",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "",
                                        "statusCode": 200,
                                        "title": "anotherSingleClass returned."
                                    }
                                ],
                                "returns": "vocab:anotherSingleClass",
                                "returnsHeader": []
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
                },
                {
                    "hydra:description": "The singleClass Class",
                    "hydra:title": "singleclass",
                    "property": {
                        "@id": "vocab:EntryPoint/singleClass",
                        "@type": "hydra:Link",
                        "description": "A non collection class",
                        "domain": "vocab:EntryPoint",
                        "label": "singleClass",
                        "range": "vocab:singleClass",
                        "supportedOperation": [
                            {
                                "@id": "updateclass",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "null",
                                "expects": "vocab:singleClass",
                                "expectsHeader": [],
                                "label": "UpdateClass",
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "",
                                        "statusCode": 200,
                                        "title": "singleClass changed."
                                    }
                                ],
                                "returns": "null",
                                "returnsHeader": []
                            },
                            {
                                "@id": "deleteclass",
                                "@type": "http://schema.org/DeleteAction",
                                "description": "null",
                                "expects": "null",
                                "expectsHeader": [],
                                "label": "DeleteClass",
                                "method": "DELETE",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "",
                                        "statusCode": 200,
                                        "title": "singleClass deleted."
                                    }
                                ],
                                "returns": "null",
                                "returnsHeader": []
                            },
                            {
                                "@id": "addclass",
                                "@type": "http://schema.org/AddAction",
                                "description": "null",
                                "expects": "vocab:singleClass",
                                "expectsHeader": [],
                                "label": "AddClass",
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "",
                                        "statusCode": 201,
                                        "title": "singleClass successfully added."
                                    }
                                ],
                                "returns": "null",
                                "returnsHeader": []
                            },
                            {
                                "@id": "getclass",
                                "@type": "http://schema.org/FindAction",
                                "description": "null",
                                "expects": "null",
                                "expectsHeader": [],
                                "label": "GetClass",
                                "method": "GET",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "",
                                        "statusCode": 200,
                                        "title": "singleClass returned."
                                    }
                                ],
                                "returns": "vocab:singleClass",
                                "returnsHeader": []
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
                },
                {
                    "hydra:description": "The extraClassCollection collection",
                    "hydra:title": "extraclasscollection",
                    "property": {
                        "@id": "vocab:EntryPoint/EcTest",
                        "@type": "hydra:Link",
                        "description": "The extraClassCollection collection",
                        "domain": "vocab:EntryPoint",
                        "label": "extraClassCollection",
                        "range": "vocab:extraClassCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:extraclass_collection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all extraClass entities",
                                "expects": "null",
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "vocab:extraClassCollection",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:extraclass_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new extraClass entity",
                                "expects": "vocab:extraClass",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "If the extraClass entity was createdsuccessfully.",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "vocab:extraClass",
                                "returnsHeader": []
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
                },
                {
                    "hydra:description": "The dummyClassCollection collection",
                    "hydra:title": "dummyclasscollection",
                    "property": {
                        "@id": "vocab:EntryPoint/DcTest",
                        "@type": "hydra:Link",
                        "description": "The dummyClassCollection collection",
                        "domain": "vocab:EntryPoint",
                        "label": "dummyClassCollection",
                        "range": "vocab:dummyClassCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:dummyclass_collection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all dummyClass entities",
                                "expects": "null",
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "vocab:dummyClassCollection",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:dummyclass_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new dummyClass entity",
                                "expects": "vocab:dummyClass",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "If the dummyClass entity was createdsuccessfully.",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "vocab:dummyClass",
                                "returnsHeader": []
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
                }
            ],
            "title": "EntryPoint"
        }
    ],
    "title": "Title for the API Documentation"
}
