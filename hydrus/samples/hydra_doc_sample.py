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
        "vocab": "petstore.swagger.io/v2/vocab#",
        "writeonly": "hydra:writeonly"
    },
    "@id": "petstore.swagger.io/v2/vocab",
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
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:Pet",
                    "method": "PUT",
                    "possibleStatus": {
                        "400": {
                            "description": "Invalid ID supplied"
                        },
                        "404": {
                            "description": "Pet not found"
                        },
                        "405": {
                            "description": "Validation exception"
                        }
                    },
                    "returns": "null",
                    "title": "Update an existing pet"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:id",
                    "readonly": "true",
                    "required": "false",
                    "title": "id",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:category",
                    "readonly": "true",
                    "required": "false",
                    "title": "category",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:name",
                    "readonly": "true",
                    "required": "false",
                    "title": "name",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:photoUrls",
                    "readonly": "true",
                    "required": "false",
                    "title": "photoUrls",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:tags",
                    "readonly": "true",
                    "required": "false",
                    "title": "tags",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:status",
                    "readonly": "true",
                    "required": "false",
                    "title": "status",
                    "writeonly": "true"
                }
            ],
            "title": "Pet"
        },
        {
            "@id": "vocab:Order",
            "@type": "hydra:Class",
            "description": "this is def",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "vocab:Order",
                    "method": "POST",
                    "possibleStatus": {
                        "200": {
                            "description": "successful operation",
                            "schema": {
                                "$ref": "#/definitions/Order"
                            }
                        },
                        "400": {
                            "description": "Invalid Order"
                        }
                    },
                    "returns": "null",
                    "title": "Place an order for a pet"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:id",
                    "readonly": "true",
                    "required": "false",
                    "title": "id",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:petId",
                    "readonly": "true",
                    "required": "false",
                    "title": "petId",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:quantity",
                    "readonly": "true",
                    "required": "false",
                    "title": "quantity",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:shipDate",
                    "readonly": "true",
                    "required": "false",
                    "title": "shipDate",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:status",
                    "readonly": "true",
                    "required": "false",
                    "title": "status",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:complete",
                    "readonly": "true",
                    "required": "false",
                    "title": "complete",
                    "writeonly": "true"
                }
            ],
            "title": "Order"
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
                    "possibleStatus": {
                        "default": {
                            "description": "successful operation"
                        }
                    },
                    "returns": "null",
                    "title": "Create user"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:id",
                    "readonly": "true",
                    "required": "false",
                    "title": "id",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:username",
                    "readonly": "true",
                    "required": "false",
                    "title": "username",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:firstName",
                    "readonly": "true",
                    "required": "false",
                    "title": "firstName",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:lastName",
                    "readonly": "true",
                    "required": "false",
                    "title": "lastName",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:email",
                    "readonly": "true",
                    "required": "false",
                    "title": "email",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:password",
                    "readonly": "true",
                    "required": "false",
                    "title": "password",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:phone",
                    "readonly": "true",
                    "required": "false",
                    "title": "phone",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:userStatus",
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
            "@id": "vocab:OrderCollection",
            "@type": "hydra:Class",
            "description": "A collection of order",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:order_collection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all Order entities",
                    "expects": "null",
                    "method": "GET",
                    "returns": "vocab:OrderCollection",
                    "statusCodes": []
                },
                {
                    "@id": "_:order_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new Order entitity",
                    "expects": "vocab:Order",
                    "method": "PUT",
                    "returns": "vocab:Order",
                    "statusCodes": [
                        {
                            "description": "If the Order entity was created successfully.",
                            "statusCode": 201
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The order",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "false",
                    "title": "members",
                    "writeonly": "false"
                }
            ],
            "title": "OrderCollection"
        },
        {
            "@id": "vocab:UserCollection",
            "@type": "hydra:Class",
            "description": "A collection of user",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:user_collection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all User entities",
                    "expects": "null",
                    "method": "GET",
                    "returns": "vocab:UserCollection",
                    "statusCodes": []
                },
                {
                    "@id": "_:user_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new User entitity",
                    "expects": "vocab:User",
                    "method": "PUT",
                    "returns": "vocab:User",
                    "statusCodes": [
                        {
                            "description": "If the User entity was created successfully.",
                            "statusCode": 201
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The user",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "false",
                    "title": "members",
                    "writeonly": "false"
                }
            ],
            "title": "UserCollection"
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
                },
                {
                    "hydra:description": "The OrderCollection collection",
                    "hydra:title": "ordercollection",
                    "property": {
                        "@id": "vocab:EntryPoint/OrderCollection",
                        "@type": "hydra:Link",
                        "description": "The OrderCollection collection",
                        "domain": "vocab:EntryPoint",
                        "label": "OrderCollection",
                        "range": "vocab:OrderCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:_:order_collection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all Order entities",
                                "expects": "null",
                                "method": "GET",
                                "returns": "vocab:OrderCollection",
                                "statusCodes": []
                            },
                            {
                                "@id": "_:_:order_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Order entitity",
                                "expects": "vocab:Order",
                                "method": "PUT",
                                "returns": "vocab:Order",
                                "statusCodes": [
                                    {
                                        "description": "If the Order entity was created successfully.",
                                        "statusCode": 201
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
                },
                {
                    "hydra:description": "The OrderCollection collection",
                    "hydra:title": "ordercollection",
                    "property": {
                        "@id": "vocab:EntryPoint/OrderCollection",
                        "@type": "hydra:Link",
                        "description": "The OrderCollection collection",
                        "domain": "vocab:EntryPoint",
                        "label": "OrderCollection",
                        "range": "vocab:OrderCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:_:order_collection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all Order entities",
                                "expects": "null",
                                "method": "GET",
                                "returns": "vocab:OrderCollection",
                                "statusCodes": []
                            },
                            {
                                "@id": "_:_:order_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Order entitity",
                                "expects": "vocab:Order",
                                "method": "PUT",
                                "returns": "vocab:Order",
                                "statusCodes": [
                                    {
                                        "description": "If the Order entity was created successfully.",
                                        "statusCode": 201
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
                    "hydra:description": "The UserCollection collection",
                    "hydra:title": "usercollection",
                    "property": {
                        "@id": "vocab:EntryPoint/UserCollection",
                        "@type": "hydra:Link",
                        "description": "The UserCollection collection",
                        "domain": "vocab:EntryPoint",
                        "label": "UserCollection",
                        "range": "vocab:UserCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:_:user_collection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all User entities",
                                "expects": "null",
                                "method": "GET",
                                "returns": "vocab:UserCollection",
                                "statusCodes": []
                            },
                            {
                                "@id": "_:_:user_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new User entitity",
                                "expects": "vocab:User",
                                "method": "PUT",
                                "returns": "vocab:User",
                                "statusCodes": [
                                    {
                                        "description": "If the User entity was created successfully.",
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
