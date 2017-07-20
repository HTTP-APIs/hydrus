"""Generated API Documentation for Drone API using drone_doc_gen.py."""

drone_doc = {
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
        "vocab": "http://localhost/droneapi/vocab#",
        "writeonly": "hydra:writeonly"
    },
    "@id": "http://localhost/droneapi/vocab",
    "@type": "ApiDocumentation",
    "description": "API Documentation for the drone side system",
    "possibleStatus": [],
    "supportedClass": [
        {
            "@id": "vocab:State",
            "@type": "hydra:Class",
            "description": "Class for drone state objects",
            "supportedOperation": [],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://auto.schema.org/speed",
                    "readonly": "true",
                    "required": "false",
                    "title": "Speed",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readonly": "true",
                    "required": "false",
                    "title": "Position",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/fuelCapacity",
                    "readonly": "true",
                    "required": "false",
                    "title": "Battery",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/status",
                    "readonly": "true",
                    "required": "false",
                    "title": "SensorStatus",
                    "writeonly": "false"
                }
            ],
            "title": "State"
        },
        {
            "@id": "vocab:Drone",
            "@type": "hydra:Class",
            "description": "Class for a drone",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "expects": "null",
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "description": "Data not found",
                            "statusCode": 404
                        },
                        {
                            "description": "State Returned",
                            "statusCode": 200
                        }
                    ],
                    "returns": "vocab:State",
                    "title": "GetState"
                },
                {
                    "@type": "hydra:Operation",
                    "expects": "vocab:State",
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "description": "State updated",
                            "statusCode": 200
                        }
                    ],
                    "returns": "null",
                    "title": "UpdateState"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:State",
                    "readonly": "true",
                    "required": "false",
                    "title": "DroneState",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/name",
                    "readonly": "true",
                    "required": "false",
                    "title": "name",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/model",
                    "readonly": "true",
                    "required": "false",
                    "title": "model",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://auto.schema.org/speed",
                    "readonly": "true",
                    "required": "false",
                    "title": "MaxSpeed",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/device",
                    "readonly": "true",
                    "required": "false",
                    "title": "Sensor",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/identifier",
                    "readonly": "true",
                    "required": "false",
                    "title": "DroneID",
                    "writeonly": "true"
                }
            ],
            "title": "Drone"
        },
        {
            "@id": "vocab:Data",
            "@type": "hydra:Class",
            "description": "Class for a data entry",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "expects": "null",
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "description": "Data not found",
                            "statusCode": 404
                        },
                        {
                            "description": "Data returned",
                            "statusCode": 200
                        }
                    ],
                    "returns": "vocab:Data",
                    "title": "GetData"
                },
                {
                    "@type": "hydra:Operation",
                    "expects": "vocab:Data",
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "description": "Data updated",
                            "statusCode": 200
                        }
                    ],
                    "returns": "null",
                    "title": "UpdateData"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/QuantitativeValue",
                    "readonly": "true",
                    "required": "false",
                    "title": "Temperature",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/identifier",
                    "readonly": "true",
                    "required": "false",
                    "title": "DroneID",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readonly": "true",
                    "required": "false",
                    "title": "Position",
                    "writeonly": "false"
                }
            ],
            "title": "Data"
        },
        {
            "@id": "vocab:Command",
            "@type": "hydra:Class",
            "description": "Class for drone commands",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "expects": "null",
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "description": "Data not found",
                            "statusCode": 404
                        },
                        {
                            "description": "Command Returned",
                            "statusCode": 200
                        }
                    ],
                    "returns": "vocab:Command",
                    "title": "GetCommand"
                },
                {
                    "@type": "hydra:Operation",
                    "expects": "vocab:Command",
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "description": "Command added",
                            "statusCode": 200
                        }
                    ],
                    "returns": "null",
                    "title": "AddCommand"
                },
                {
                    "@type": "hydra:Operation",
                    "expects": "null",
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "description": "Command deleted",
                            "statusCode": 200
                        }
                    ],
                    "returns": "null",
                    "title": "DeleteCommand"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/UpdateAction",
                    "readonly": "false",
                    "required": "false",
                    "title": "Update",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:State",
                    "readonly": "false",
                    "required": "false",
                    "title": "State",
                    "writeonly": "false"
                }
            ],
            "title": "Command"
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
            "@id": "vocab:CommandCollection",
            "@type": "hydra:Class",
            "description": "A collection of command",
            "label": "CommandCollection",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:command_collection_retrieve",
                    "@type": "hydra:Operation",
                    "description": "Retrieves all Command entities",
                    "expects": "null",
                    "method": "GET",
                    "returns": "vocab:CommandCollection",
                    "statusCodes": []
                },
                {
                    "@id": "_:command_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new Command entitity",
                    "expects": "vocab:Command",
                    "method": "PUT",
                    "returns": "vocab:Command",
                    "statusCodes": [
                        {
                            "description": "If the Command entity was created successfully.",
                            "statusCode": 201
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The command",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "false",
                    "title": "members",
                    "writeonly": "false"
                }
            ]
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
                    "hydra:description": "The Drone Class",
                    "hydra:title": "drone",
                    "property": {
                        "@id": "vocab:EntryPoint/Drone",
                        "@type": "hydra:Link",
                        "description": "Class for a drone",
                        "domain": "vocab:EntryPoint",
                        "label": "Drone",
                        "range": "vocab:Drone",
                        "supportedOperation": [
                            {
                                "@id": "_:getstate",
                                "@type": "hydra:Operation",
                                "description": "null",
                                "expects": "null",
                                "label": "GetState",
                                "method": "GET",
                                "returns": "vocab:State",
                                "statusCodes": [
                                    {
                                        "description": "Data not found",
                                        "statusCode": 404
                                    },
                                    {
                                        "description": "State Returned",
                                        "statusCode": 200
                                    }
                                ]
                            },
                            {
                                "@id": "_:updatestate",
                                "@type": "hydra:Operation",
                                "description": "null",
                                "expects": "vocab:State",
                                "label": "UpdateState",
                                "method": "POST",
                                "returns": "null",
                                "statusCodes": [
                                    {
                                        "description": "State updated",
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
                    "hydra:description": "The Data Class",
                    "hydra:title": "data",
                    "property": {
                        "@id": "vocab:EntryPoint/Data",
                        "@type": "hydra:Link",
                        "description": "Class for a data entry",
                        "domain": "vocab:EntryPoint",
                        "label": "Data",
                        "range": "vocab:Data",
                        "supportedOperation": [
                            {
                                "@id": "_:getdata",
                                "@type": "hydra:Operation",
                                "description": "null",
                                "expects": "null",
                                "label": "GetData",
                                "method": "GET",
                                "returns": "vocab:Data",
                                "statusCodes": [
                                    {
                                        "description": "Data not found",
                                        "statusCode": 404
                                    },
                                    {
                                        "description": "Data returned",
                                        "statusCode": 200
                                    }
                                ]
                            },
                            {
                                "@id": "_:updatedata",
                                "@type": "hydra:Operation",
                                "description": "null",
                                "expects": "vocab:Data",
                                "label": "UpdateData",
                                "method": "POST",
                                "returns": "null",
                                "statusCodes": [
                                    {
                                        "description": "Data updated",
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
                    "hydra:description": "The CommandCollection collection",
                    "hydra:title": "commandcollection",
                    "property": {
                        "@id": "vocab:EntryPoint/CommandCollection",
                        "@type": "hydra:Link",
                        "description": "The CommandCollection collection",
                        "domain": "vocab:EntryPoint",
                        "label": "CommandCollection",
                        "range": "vocab:CommandCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:_:command_collection_retrieve",
                                "@type": "hydra:Operation",
                                "description": "Retrieves all Command entities",
                                "expects": "null",
                                "method": "GET",
                                "returns": "vocab:CommandCollection",
                                "statusCodes": []
                            },
                            {
                                "@id": "_:_:command_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Command entitity",
                                "expects": "vocab:Command",
                                "method": "PUT",
                                "returns": "vocab:Command",
                                "statusCodes": [
                                    {
                                        "description": "If the Command entity was created successfully.",
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
    ]
}