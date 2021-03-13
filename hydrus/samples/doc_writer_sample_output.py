"""Generated API Documentation sample using doc_writer_sample.py."""
    
doc = {
    "@context": {
        "ApiDocumentation": "hydra:ApiDocumentation",
        "description": "hydra:description",
        "domain": {
            "@id": "rdfs:domain",
            "@type": "@id"
        },
        "entrypoint": {
            "@id": "hydra:entrypoint",
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
        "object": {
            "@id": "hydra:object",
            "@type": "@id"
        },
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
        "search": "hydra:search",
        "statusCode": "hydra:statusCode",
        "subClassOf": {
            "@id": "rdfs:subClassOf",
            "@type": "@id"
        },
        "subject": {
            "@id": "hydra:subject",
            "@type": "@id"
        },
        "supportedClass": "hydra:supportedClass",
        "supportedOperation": "hydra:supportedOperation",
        "supportedProperty": "hydra:supportedProperty",
        "title": "hydra:title",
        "writeable": "hydra:writeable"
    },
    "@id": "http://hydrus.com/api/vocab",
    "@type": "ApiDocumentation",
    "description": "Description for the API Documentation",
    "entrypoint": "http://hydrus.com/api",
    "possibleStatus": [],
    "supportedClass": [
        {
            "@id": "http://hydrus.com/api/vocab#dummyClass",
            "@type": "hydra:Class",
            "description": "A dummyClass for demo",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "http://hydrus.com/api/vocab#dummyClass",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "dummyClass updated.",
                            "statusCode": 200,
                            "title": ""
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
                            "description": "dummyClass deleted.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [],
                    "title": "DeleteClass"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "http://hydrus.com/api/vocab#dummyClass",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "dummyClass successfully added.",
                            "statusCode": 201,
                            "title": ""
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
                            "description": "dummyClass returned.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://hydrus.com/api/vocab#dummyClass",
                    "returnsHeader": [],
                    "title": "GetClass"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://props.hydrus.com/prop1",
                    "readable": "false",
                    "required": "false",
                    "title": "Prop1",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://props.hydrus.com/prop2",
                    "readable": "false",
                    "required": "false",
                    "title": "Prop2",
                    "writeable": "true"
                }
            ],
            "title": "dummyClass"
        },
        {
            "@id": "http://hydrus.com/api/vocab#extraClass",
            "@type": "hydra:Class",
            "description": "Class without any explicit methods",
            "supportedOperation": [],
            "supportedProperty": [],
            "title": "extraClass"
        },
        {
            "@id": "http://hydrus.com/api/vocab#singleClass",
            "@type": "hydra:Class",
            "description": "A non collection class",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "http://hydrus.com/api/vocab#singleClass",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "singleClass changed.",
                            "statusCode": 200,
                            "title": ""
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
                            "description": "singleClass deleted.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [],
                    "title": "DeleteClass"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "http://hydrus.com/api/vocab#singleClass",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "singleClass successfully added.",
                            "statusCode": 201,
                            "title": ""
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
                            "description": "singleClass returned.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://hydrus.com/api/vocab#singleClass",
                    "returnsHeader": [],
                    "title": "GetClass"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://props.hydrus.com/prop1",
                    "readable": "false",
                    "required": "false",
                    "title": "Prop1",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://props.hydrus.com/prop2",
                    "readable": "false",
                    "required": "false",
                    "title": "Prop2",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": {
                        "@id": "http://hydrus.com/api/vocab#singleClass/dummyProp",
                        "@type": "hydra:Link",
                        "description": "",
                        "domain": "http://hydrus.com/api/vocab#singleClass",
                        "range": "http://hydrus.com/api/vocab#dummyClass",
                        "supportedOperation": [],
                        "title": "dummyProp"
                    },
                    "readable": "false",
                    "required": "false",
                    "title": "dummyProp",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://hydrus.com/api/vocab#anotherSingleClass",
                    "readable": "false",
                    "required": "false",
                    "title": "singleClassProp",
                    "writeable": "true"
                }
            ],
            "title": "singleClass"
        },
        {
            "@id": "http://hydrus.com/api/vocab#anotherSingleClass",
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
                            "description": "anotherSingleClass returned.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://hydrus.com/api/vocab#anotherSingleClass",
                    "returnsHeader": [],
                    "title": "GetClass"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://props.hydrus.com/prop1",
                    "readable": "false",
                    "required": "false",
                    "title": "Prop1",
                    "writeable": "true"
                }
            ],
            "title": "anotherSingleClass"
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
            "@id": "http://hydrus.com/api/vocab#Extraclasses",
            "@type": "Collection",
            "description": "This collection comprises of instances of ExtraClass",
            "manages": {
                "object": "http://hydrus.com/api/vocab#extraClass",
                "property": "rdf:type"
            },
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:Extraclasses_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all the members of Extraclasses",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "http://hydrus.com/api/vocab#extraClass",
                    "returnsHeader": []
                },
                {
                    "@id": "_:Extraclasses_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new member in Extraclasses",
                    "expects": "http://hydrus.com/api/vocab#extraClass",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "A new member in Extraclasses created",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "http://hydrus.com/api/vocab#extraClass",
                    "returnsHeader": []
                },
                {
                    "@id": "_:Extraclasses_update",
                    "@type": "http://schema.org/UpdateAction",
                    "description": "Update member of  Extraclasses ",
                    "expects": "http://hydrus.com/api/vocab#extraClass",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "If the entity was updatedfrom Extraclasses.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://hydrus.com/api/vocab#extraClass",
                    "returnsHeader": []
                },
                {
                    "@id": "_:Extraclasses_delete",
                    "@type": "http://schema.org/DeleteAction",
                    "description": "Delete member of Extraclasses ",
                    "expects": "http://hydrus.com/api/vocab#extraClass",
                    "expectsHeader": [],
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "If entity was deletedsuccessfully from Extraclasses.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://hydrus.com/api/vocab#extraClass",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The members of Extraclasses",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "false",
                    "required": "false",
                    "title": "members",
                    "writeable": "false"
                }
            ],
            "title": "Extraclasses"
        },
        {
            "@id": "http://hydrus.com/api/vocab#dummyclasses",
            "@type": "Collection",
            "description": "This collection comprises of instances of dummyClass",
            "manages": {
                "object": "http://hydrus.com/api/vocab#dummyClass",
                "property": "rdf:type"
            },
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:dummyclasses_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all the members of dummyclasses",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "http://hydrus.com/api/vocab#dummyClass",
                    "returnsHeader": []
                },
                {
                    "@id": "_:dummyclasses_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new member in dummyclasses",
                    "expects": "http://hydrus.com/api/vocab#dummyClass",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "A new member in dummyclasses created",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "http://hydrus.com/api/vocab#dummyClass",
                    "returnsHeader": []
                },
                {
                    "@id": "_:dummyclasses_update",
                    "@type": "http://schema.org/UpdateAction",
                    "description": "Update member of  dummyclasses ",
                    "expects": "http://hydrus.com/api/vocab#dummyClass",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "If the entity was updatedfrom dummyclasses.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://hydrus.com/api/vocab#dummyClass",
                    "returnsHeader": []
                },
                {
                    "@id": "_:dummyclasses_delete",
                    "@type": "http://schema.org/DeleteAction",
                    "description": "Delete member of dummyclasses ",
                    "expects": "http://hydrus.com/api/vocab#dummyClass",
                    "expectsHeader": [],
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "If entity was deletedsuccessfully from dummyclasses.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://hydrus.com/api/vocab#dummyClass",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The members of dummyclasses",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "false",
                    "required": "false",
                    "title": "members",
                    "writeable": "false"
                }
            ],
            "title": "dummyclasses"
        },
        {
            "@id": "http://hydrus.com/api#EntryPoint",
            "@type": "hydra:Class",
            "description": "The main entry point or homepage of the API.",
            "supportedOperation": [
                {
                    "@id": "_:entry_point",
                    "@type": "http://hydrus.com//api#EntryPoint",
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
                    "hydra:description": "The singleClass Class",
                    "hydra:title": "singleclass",
                    "property": {
                        "@id": "http://hydrus.com/api/vocab#EntryPoint/singleClass",
                        "@type": "hydra:Link",
                        "description": "A non collection class",
                        "domain": "http://hydrus.com/api/vocab#EntryPoint",
                        "label": "singleClass",
                        "range": "http://hydrus.com/api/vocab#singleClass",
                        "supportedOperation": [
                            {
                                "@id": "updateclass",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "null",
                                "expects": "http://hydrus.com/api/vocab#singleClass",
                                "expectsHeader": [],
                                "label": "UpdateClass",
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "singleClass changed.",
                                        "statusCode": 200,
                                        "title": ""
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
                                        "description": "singleClass deleted.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "null",
                                "returnsHeader": []
                            },
                            {
                                "@id": "addclass",
                                "@type": "http://schema.org/AddAction",
                                "description": "null",
                                "expects": "http://hydrus.com/api/vocab#singleClass",
                                "expectsHeader": [],
                                "label": "AddClass",
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "singleClass successfully added.",
                                        "statusCode": 201,
                                        "title": ""
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
                                        "description": "singleClass returned.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://hydrus.com/api/vocab#singleClass",
                                "returnsHeader": []
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
                },
                {
                    "hydra:description": "The anotherSingleClass Class",
                    "hydra:title": "anothersingleclass",
                    "property": {
                        "@id": "http://hydrus.com/api/vocab#EntryPoint/anotherSingleClass",
                        "@type": "hydra:Link",
                        "description": "An another non collection class",
                        "domain": "http://hydrus.com/api/vocab#EntryPoint",
                        "label": "anotherSingleClass",
                        "range": "http://hydrus.com/api/vocab#anotherSingleClass",
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
                                        "description": "anotherSingleClass returned.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://hydrus.com/api/vocab#anotherSingleClass",
                                "returnsHeader": []
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
                },
                {
                    "hydra:description": "The Extraclasses collection",
                    "hydra:title": "extraclasses",
                    "property": {
                        "@id": "http://hydrus.com/api/vocab#EntryPoint/EcTest",
                        "@type": "hydra:Link",
                        "description": "The Extraclasses collection",
                        "domain": "http://hydrus.com/api/vocab#EntryPoint",
                        "label": "Extraclasses",
                        "manages": {
                            "object": "http://hydrus.com/api/vocab#extraClass",
                            "property": "rdf:type"
                        },
                        "range": "http://hydrus.com/api/vocab#Extraclasses",
                        "supportedOperation": [
                            {
                                "@id": "_:extraclasses_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all the members of Extraclasses",
                                "expects": "null",
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "http://hydrus.com/api/vocab#extraClass",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:extraclasses_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new member in Extraclasses",
                                "expects": "http://hydrus.com/api/vocab#extraClass",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "A new member in Extraclasses created",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://hydrus.com/api/vocab#extraClass",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:extraclasses_update",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "Update member of  Extraclasses ",
                                "expects": "http://hydrus.com/api/vocab#extraClass",
                                "expectsHeader": [],
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "If the entity was updatedfrom Extraclasses.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://hydrus.com/api/vocab#extraClass",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:extraclasses_delete",
                                "@type": "http://schema.org/DeleteAction",
                                "description": "Delete member of Extraclasses ",
                                "expects": "http://hydrus.com/api/vocab#extraClass",
                                "expectsHeader": [],
                                "method": "DELETE",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "If entity was deletedsuccessfully from Extraclasses.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://hydrus.com/api/vocab#extraClass",
                                "returnsHeader": []
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
                },
                {
                    "hydra:description": "The dummyclasses collection",
                    "hydra:title": "dummyclasses",
                    "property": {
                        "@id": "http://hydrus.com/api/vocab#EntryPoint/DcTest",
                        "@type": "hydra:Link",
                        "description": "The dummyclasses collection",
                        "domain": "http://hydrus.com/api/vocab#EntryPoint",
                        "label": "dummyclasses",
                        "manages": {
                            "object": "http://hydrus.com/api/vocab#dummyClass",
                            "property": "rdf:type"
                        },
                        "range": "http://hydrus.com/api/vocab#dummyclasses",
                        "supportedOperation": [
                            {
                                "@id": "_:dummyclasses_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all the members of dummyclasses",
                                "expects": "null",
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "http://hydrus.com/api/vocab#dummyClass",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:dummyclasses_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new member in dummyclasses",
                                "expects": "http://hydrus.com/api/vocab#dummyClass",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "A new member in dummyclasses created",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://hydrus.com/api/vocab#dummyClass",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:dummyclasses_update",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "Update member of  dummyclasses ",
                                "expects": "http://hydrus.com/api/vocab#dummyClass",
                                "expectsHeader": [],
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "If the entity was updatedfrom dummyclasses.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://hydrus.com/api/vocab#dummyClass",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:dummyclasses_delete",
                                "@type": "http://schema.org/DeleteAction",
                                "description": "Delete member of dummyclasses ",
                                "expects": "http://hydrus.com/api/vocab#dummyClass",
                                "expectsHeader": [],
                                "method": "DELETE",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "If entity was deletedsuccessfully from dummyclasses.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://hydrus.com/api/vocab#dummyClass",
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
