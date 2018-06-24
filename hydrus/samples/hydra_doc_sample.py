"""
Generated API Documentation for Server API using server_doc_gen.py."""

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
        "vocab": "http://petstore.swagger.io/v2/vocab#",
        "writeonly": "hydra:writeonly"
    },
    "@id": "http://petstore.swagger.io/v2/vocab",
    "@type": "ApiDocumentation",
    "description": "This is a sample server Petstore server.  You can find out more about Swagger at [http://swagger.io](http://swagger.io) or on [irc.freenode.net, #swagger](http://swagger.io/irc/).  For this sample, you can use the api key `special-key` to test the authorization filters.",
    "possibleStatus": [],
    "supportedClass": [
        {
            "@id": "vocab:Pet",
            "@type": "hydra:Class",
            "description": "Pet",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "vocab:Pet",
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "description": "Invalid input",
                            "statusCode": 405
                        }
                    ],
                    "returns": "null",
                    "title": "Add a new pet to the store"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:Pet",
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "description": "Invalid ID supplied",
                            "statusCode": 400
                        }
                    ],
                    "returns": "null",
                    "title": "Update an existing pet"
                },
                {
                    "@type": "http://schema.org/FindAction",
                    "expects": "null",
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "description": "successful operation",
                            "statusCode": 200
                        }
                    ],
                    "returns": "vocab:Pet",
                    "title": "get all pets"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/Integer",
                    "readonly": "true",
                    "required": "false",
                    "title": "id",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:Category",
                    "readonly": "true",
                    "required": "false",
                    "title": "category",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/Text",
                    "readonly": "true",
                    "required": "true",
                    "title": "name",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "0",
                    "readonly": "true",
                    "required": "true",
                    "title": "photoUrls",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "0",
                    "readonly": "true",
                    "required": "false",
                    "title": "tags",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/Text",
                    "readonly": "true",
                    "required": "false",
                    "title": "status",
                    "writeonly": "true"
                }
            ],
            "title": "Pet"
        },
        {
            "@id": "vocab:User",
            "@type": "hydra:Class",
            "description": "User",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "vocab:User",
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "description": "Successful Operation",
                            "statusCode": 200
                        }
                    ],
                    "returns": "null",
                    "title": "Create user"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/Integer",
                    "readonly": "true",
                    "required": "false",
                    "title": "id",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/Text",
                    "readonly": "true",
                    "required": "false",
                    "title": "username",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/Text",
                    "readonly": "true",
                    "required": "false",
                    "title": "firstName",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/Text",
                    "readonly": "true",
                    "required": "false",
                    "title": "lastName",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/Text",
                    "readonly": "true",
                    "required": "false",
                    "title": "email",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:xyz",
                    "readonly": "true",
                    "required": "false",
                    "title": "xyz",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/Text",
                    "readonly": "true",
                    "required": "false",
                    "title": "password",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/Text",
                    "readonly": "true",
                    "required": "false",
                    "title": "phone",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/Integer",
                    "readonly": "true",
                    "required": "false",
                    "title": "userStatus",
                    "writeonly": "true"
                }
            ],
            "title": "User"
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
            "@id": "http://www.w3.org/ns/hydra/core#Resource",
            "@type": "hydra:Class",
            "description": "null",
            "supportedOperation": [],
            "supportedProperty": [],
            "title": "Resource"
        },
        {
            "@id": "vocab:PetCollection",
            "@type": "hydra:Class",
            "description": "A collection of pet",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:pet_collection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all Pet entities",
                    "expects": "null",
                    "method": "GET",
                    "returns": "vocab:PetCollection",
                    "statusCodes": []
                },
                {
                    "@id": "_:pet_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new Pet entitity",
                    "expects": "vocab:Pet",
                    "method": "PUT",
                    "returns": "vocab:Pet",
                    "statusCodes": [
                        {
                            "description": "If the Pet entity was created successfully.",
                            "statusCode": 201
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The pet",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "false",
                    "title": "members",
                    "writeonly": "false"
                }
            ],
            "title": "PetCollection"
        },
        {
            "@id": "vocab:EntryPoint",
            "@type": "hydra:Class",
            "description": "The main entry point or homepage of the API.",
            "supportedOperation": [
                {
                    "@id": "_:entry_point",
                    "@type": "http://schema.org/FindAction",
                    "description": "The APIs main entry point.",
                    "expects": "null",
                    "method": "GET",
                    "returns": "null",
                    "statusCodes": "vocab:EntryPoint"
                }
            ],
            "supportedProperty": [
                {
                    "hydra:description": "The Pet Class",
                    "hydra:title": "pet",
                    "property": {
                        "@id": "vocab:EntryPoint/Pet",
                        "@type": "hydra:Link",
                        "description": "Pet",
                        "domain": "vocab:EntryPoint",
                        "label": "Pet",
                        "range": "vocab:Pet",
                        "supportedOperation": [
                            {
                                "@id": "_:add a new pet to the store",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "null",
                                "expects": "vocab:Pet",
                                "label": "Add a new pet to the store",
                                "method": "POST",
                                "returns": "null",
                                "statusCodes": [
                                    {
                                        "description": "Invalid input",
                                        "statusCode": 405
                                    }
                                ]
                            },
                            {
                                "@id": "_:update an existing pet",
                                "@type": "http://schema.org/AddAction",
                                "description": "null",
                                "expects": "vocab:Pet",
                                "label": "Update an existing pet",
                                "method": "PUT",
                                "returns": "null",
                                "statusCodes": [
                                    {
                                        "description": "Invalid ID supplied",
                                        "statusCode": 400
                                    }
                                ]
                            },
                            {
                                "@id": "_:get all pets",
                                "@type": "http://schema.org/FindAction",
                                "description": "null",
                                "expects": "null",
                                "label": "get all pets",
                                "method": "GET",
                                "returns": "vocab:Pet",
                                "statusCodes": [
                                    {
                                        "description": "successful operation",
                                        "statusCode": 200
                                    }
                                ]
                            }
                        ]
                    },
                    "readonly": "true",
                    "required": "null",
                    "writeonly": "false"
                },
                {
                    "hydra:description": "The User Class",
                    "hydra:title": "user",
                    "property": {
                        "@id": "vocab:EntryPoint/User",
                        "@type": "hydra:Link",
                        "description": "User",
                        "domain": "vocab:EntryPoint",
                        "label": "User",
                        "range": "vocab:User",
                        "supportedOperation": [
                            {
                                "@id": "_:create user",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "null",
                                "expects": "vocab:User",
                                "label": "Create user",
                                "method": "POST",
                                "returns": "null",
                                "statusCodes": [
                                    {
                                        "description": "Successful Operation",
                                        "statusCode": 200
                                    }
                                ]
                            }
                        ]
                    },
                    "readonly": "true",
                    "required": "null",
                    "writeonly": "false"
                },
                {
                    "hydra:description": "The PetCollection collection",
                    "hydra:title": "petcollection",
                    "property": {
                        "@id": "vocab:EntryPoint/PetCollection",
                        "@type": "hydra:Link",
                        "description": "The PetCollection collection",
                        "domain": "vocab:EntryPoint",
                        "label": "PetCollection",
                        "range": "vocab:PetCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:_:pet_collection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all Pet entities",
                                "expects": "null",
                                "method": "GET",
                                "returns": "vocab:PetCollection",
                                "statusCodes": []
                            },
                            {
                                "@id": "_:_:pet_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Pet entitity",
                                "expects": "vocab:Pet",
                                "method": "PUT",
                                "returns": "vocab:Pet",
                                "statusCodes": [
                                    {
                                        "description": "If the Pet entity was created successfully.",
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
    "title": "Swagger Petstore"
}
