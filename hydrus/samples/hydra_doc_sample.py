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
        "vocab": "http://localhost:8080/api/vocab#",
        "writeonly": "hydra:writeonly"
    },
    "@id": "http://localhost:8080/api/vocab",
    "@type": "ApiDocumentation",
    "description": "API Documentation for the server side system",
    "possibleStatus": [],
    "supportedClass": [
        {
            "@id": "vocab:State",
            "@type": "hydra:Class",
            "description": "Class for drone state objects",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/FindAction",
                    "expects": "null",
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "description": "State not found",
                            "statusCode": 404
                        },
                        {
                            "description": "State Returned",
                            "statusCode": 200
                        }
                    ],
                    "returns": "vocab:State",
                    "title": "GetState"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://auto.schema.org/speed",
                    "readonly": "false",
                    "required": "true",
                    "title": "Speed",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readonly": "false",
                    "required": "true",
                    "title": "Position",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/Property",
                    "readonly": "false",
                    "required": "true",
                    "title": "Direction",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/fuelCapacity",
                    "readonly": "false",
                    "required": "true",
                    "title": "Battery",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/status",
                    "readonly": "false",
                    "required": "true",
                    "title": "SensorStatus",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/identifier",
                    "readonly": "false",
                    "required": "true",
                    "title": "DroneID",
                    "writeonly": "false"
                }
            ],
            "title": "State"
        },
        {
            "@id": "vocab:Command",
            "@type": "hydra:Class",
            "description": "Class for drone commands",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/FindAction",
                    "expects": "null",
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "description": "Command not found",
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
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:Command",
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "description": "Command added",
                            "statusCode": 201
                        }
                    ],
                    "returns": "null",
                    "title": "AddCommand"
                },
                {
                    "@type": "http://schema.org/DeleteAction",
                    "expects": "null",
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "description": "Command deleted",
                            "statusCode": 201
                        }
                    ],
                    "returns": "null",
                    "title": "DeleteCommand"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/identifier",
                    "readonly": "false",
                    "required": "true",
                    "title": "DroneID",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:State",
                    "readonly": "false",
                    "required": "true",
                    "title": "State",
                    "writeonly": "false"
                }
            ],
            "title": "Command"
        },
        {
            "@id": "vocab:Message",
            "@type": "hydra:Class",
            "description": "Class for messages received by the GUI interface",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/FindAction",
                    "expects": "null",
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "description": "Message not found",
                            "statusCode": 404
                        },
                        {
                            "description": "Message returned",
                            "statusCode": 200
                        }
                    ],
                    "returns": "vocab:Message",
                    "title": "GetMessage"
                },
                {
                    "@type": "http://schema.org/DeleteAction",
                    "expects": "null",
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "description": "Message deleted",
                            "statusCode": 200
                        }
                    ],
                    "returns": "null",
                    "title": "DeleteMessage"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/Text",
                    "readonly": "false",
                    "required": "true",
                    "title": "MessageString",
                    "writeonly": "false"
                }
            ],
            "title": "Message"
        },
        {
            "@id": "vocab:Area",
            "@type": "hydra:Class",
            "description": "Class for Area of Interest of the server",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "vocab:Area",
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "description": "Area of interest changed",
                            "statusCode": 200
                        }
                    ],
                    "returns": "null",
                    "title": "UpdateArea"
                },
                {
                    "@type": "http://schema.org/FindAction",
                    "expects": "null",
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "description": "Area of interest not found",
                            "statusCode": 404
                        },
                        {
                            "description": "Area of interest returned",
                            "statusCode": 200
                        }
                    ],
                    "returns": "vocab:Area",
                    "title": "GetArea"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readonly": "false",
                    "required": "true",
                    "title": "TopLeft",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readonly": "false",
                    "required": "true",
                    "title": "BottomRight",
                    "writeonly": "false"
                }
            ],
            "title": "Area"
        },
        {
            "@id": "vocab:Datastream",
            "@type": "hydra:Class",
            "description": "Class for a datastream entry",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/FindAction",
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
                    "returns": "vocab:Datastream",
                    "title": "ReadDatastream"
                },
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "vocab:Datastream",
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "description": "Data updated",
                            "statusCode": 200
                        }
                    ],
                    "returns": "null",
                    "title": "UpdateDatastream"
                },
                {
                    "@type": "http://schema.org/DeleteAction",
                    "expects": "null",
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "description": "Data deleted",
                            "statusCode": 200
                        }
                    ],
                    "returns": "null",
                    "title": "DeleteDatastream"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/QuantitativeValue",
                    "readonly": "false",
                    "required": "true",
                    "title": "Temperature",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/identifier",
                    "readonly": "false",
                    "required": "true",
                    "title": "DroneID",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readonly": "false",
                    "required": "true",
                    "title": "Position",
                    "writeonly": "false"
                }
            ],
            "title": "Datastream"
        },
        {
            "@id": "vocab:Drone",
            "@type": "hydra:Class",
            "description": "Class for a drone",
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
                    "title": "SubmitDrone"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:Drone",
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "description": "Drone added",
                            "statusCode": 200
                        }
                    ],
                    "returns": "null",
                    "title": "CreateDrone"
                },
                {
                    "@type": "http://schema.org/FindAction",
                    "expects": "null",
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "description": "Drone not found",
                            "statusCode": 404
                        },
                        {
                            "description": "Drone Returned",
                            "statusCode": 200
                        }
                    ],
                    "returns": "vocab:Drone",
                    "title": "GetDrone"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:State",
                    "readonly": "false",
                    "required": "true",
                    "title": "DroneState",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/name",
                    "readonly": "false",
                    "required": "true",
                    "title": "name",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/model",
                    "readonly": "false",
                    "required": "true",
                    "title": "model",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://auto.schema.org/speed",
                    "readonly": "false",
                    "required": "true",
                    "title": "MaxSpeed",
                    "writeonly": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/device",
                    "readonly": "false",
                    "required": "true",
                    "title": "Sensor",
                    "writeonly": "false"
                }
            ],
            "title": "Drone"
        },
        {
            "@id": "vocab:LogEntry",
            "@type": "hydra:Class",
            "description": "Class for a log entry",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/FindAction",
                    "expects": "null",
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "description": "Log entry not found",
                            "statusCode": 404
                        },
                        {
                            "description": "Log entry returned",
                            "statusCode": 200
                        }
                    ],
                    "returns": "vocab:LogEntry",
                    "title": "GetLog"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:LogEntry",
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "description": "Log entry created",
                            "statusCode": 201
                        }
                    ],
                    "returns": "null",
                    "title": "AddLog"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/identifier",
                    "readonly": "true",
                    "required": "false",
                    "title": "DroneID",
                    "writeonly": "true"
                },
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
                    "property": "http://schema.org/ReplyAction",
                    "readonly": "false",
                    "required": "false",
                    "title": "Get",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/SendAction",
                    "readonly": "false",
                    "required": "false",
                    "title": "Send",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:State",
                    "readonly": "false",
                    "required": "false",
                    "title": "State",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:Datastream",
                    "readonly": "false",
                    "required": "false",
                    "title": "Data",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:Command",
                    "readonly": "false",
                    "required": "false",
                    "title": "Command",
                    "writeonly": "true"
                }
            ],
            "title": "LogEntry"
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
            "@id": "vocab:CommandCollection",
            "@type": "hydra:Class",
            "description": "A collection of command",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:command_collection_retrieve",
                    "@type": "http://schema.org/FindAction",
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
            ],
            "title": "CommandCollection"
        },
        {
            "@id": "vocab:StateCollection",
            "@type": "hydra:Class",
            "description": "A collection of state",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:state_collection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all State entities",
                    "expects": "null",
                    "method": "GET",
                    "returns": "vocab:StateCollection",
                    "statusCodes": []
                },
                {
                    "@id": "_:state_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new State entitity",
                    "expects": "vocab:State",
                    "method": "PUT",
                    "returns": "vocab:State",
                    "statusCodes": [
                        {
                            "description": "If the State entity was created successfully.",
                            "statusCode": 201
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The state",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "false",
                    "title": "members",
                    "writeonly": "false"
                }
            ],
            "title": "StateCollection"
        },
        {
            "@id": "vocab:MessageCollection",
            "@type": "hydra:Class",
            "description": "A collection of message",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:message_collection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all Message entities",
                    "expects": "null",
                    "method": "GET",
                    "returns": "vocab:MessageCollection",
                    "statusCodes": []
                },
                {
                    "@id": "_:message_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new Message entitity",
                    "expects": "vocab:Message",
                    "method": "PUT",
                    "returns": "vocab:Message",
                    "statusCodes": [
                        {
                            "description": "If the Message entity was created successfully.",
                            "statusCode": 201
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The message",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "false",
                    "title": "members",
                    "writeonly": "false"
                }
            ],
            "title": "MessageCollection"
        },
        {
            "@id": "vocab:DroneCollection",
            "@type": "hydra:Class",
            "description": "A collection of drone",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:drone_collection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all Drone entities",
                    "expects": "null",
                    "method": "GET",
                    "returns": "vocab:DroneCollection",
                    "statusCodes": []
                },
                {
                    "@id": "_:drone_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new Drone entitity",
                    "expects": "vocab:Drone",
                    "method": "PUT",
                    "returns": "vocab:Drone",
                    "statusCodes": [
                        {
                            "description": "If the Drone entity was created successfully.",
                            "statusCode": 201
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The drone",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "false",
                    "title": "members",
                    "writeonly": "false"
                }
            ],
            "title": "DroneCollection"
        },
        {
            "@id": "vocab:LogEntryCollection",
            "@type": "hydra:Class",
            "description": "A collection of logentry",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:logentry_collection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all LogEntry entities",
                    "expects": "null",
                    "method": "GET",
                    "returns": "vocab:LogEntryCollection",
                    "statusCodes": []
                },
                {
                    "@id": "_:logentry_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new LogEntry entitity",
                    "expects": "vocab:LogEntry",
                    "method": "PUT",
                    "returns": "vocab:LogEntry",
                    "statusCodes": [
                        {
                            "description": "If the LogEntry entity was created successfully.",
                            "statusCode": 201
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The logentry",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "false",
                    "title": "members",
                    "writeonly": "false"
                }
            ],
            "title": "LogEntryCollection"
        },
        {
            "@id": "vocab:DatastreamCollection",
            "@type": "hydra:Class",
            "description": "A collection of datastream",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:datastream_collection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all Datastream entities",
                    "expects": "null",
                    "method": "GET",
                    "returns": "vocab:DatastreamCollection",
                    "statusCodes": []
                },
                {
                    "@id": "_:datastream_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new Datastream entitity",
                    "expects": "vocab:Datastream",
                    "method": "PUT",
                    "returns": "vocab:Datastream",
                    "statusCodes": [
                        {
                            "description": "If the Datastream entity was created successfully.",
                            "statusCode": 201
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The datastream",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "false",
                    "title": "members",
                    "writeonly": "false"
                }
            ],
            "title": "DatastreamCollection"
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
                    "hydra:description": "The Area Class",
                    "hydra:title": "area",
                    "property": {
                        "@id": "vocab:EntryPoint/Area",
                        "@type": "hydra:Link",
                        "description": "Class for Area of Interest of the server",
                        "domain": "vocab:EntryPoint",
                        "label": "Area",
                        "range": "vocab:Area",
                        "supportedOperation": [
                            {
                                "@id": "updatearea",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "null",
                                "expects": "vocab:Area",
                                "label": "UpdateArea",
                                "method": "POST",
                                "returns": "null",
                                "statusCodes": [
                                    {
                                        "description": "Area of interest changed",
                                        "statusCode": 200
                                    }
                                ]
                            },
                            {
                                "@id": "getarea",
                                "@type": "http://schema.org/FindAction",
                                "description": "null",
                                "expects": "null",
                                "label": "GetArea",
                                "method": "GET",
                                "returns": "vocab:Area",
                                "statusCodes": [
                                    {
                                        "description": "Area of interest not found",
                                        "statusCode": 404
                                    },
                                    {
                                        "description": "Area of interest returned",
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
                                "@id": "_:command_collection_retrieve",
                                "@type": "http://schema.org/FindAction",
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
                        ]
                    },
                    "readonly": "true",
                    "required": "null",
                    "writeonly": "false"
                },
                {
                    "hydra:description": "The StateCollection collection",
                    "hydra:title": "statecollection",
                    "property": {
                        "@id": "vocab:EntryPoint/StateCollection",
                        "@type": "hydra:Link",
                        "description": "The StateCollection collection",
                        "domain": "vocab:EntryPoint",
                        "label": "StateCollection",
                        "range": "vocab:StateCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:state_collection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all State entities",
                                "expects": "null",
                                "method": "GET",
                                "returns": "vocab:StateCollection",
                                "statusCodes": []
                            },
                            {
                                "@id": "_:state_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new State entitity",
                                "expects": "vocab:State",
                                "method": "PUT",
                                "returns": "vocab:State",
                                "statusCodes": [
                                    {
                                        "description": "If the State entity was created successfully.",
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
                    "hydra:description": "The MessageCollection collection",
                    "hydra:title": "messagecollection",
                    "property": {
                        "@id": "vocab:EntryPoint/MessageCollection",
                        "@type": "hydra:Link",
                        "description": "The MessageCollection collection",
                        "domain": "vocab:EntryPoint",
                        "label": "MessageCollection",
                        "range": "vocab:MessageCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:message_collection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all Message entities",
                                "expects": "null",
                                "method": "GET",
                                "returns": "vocab:MessageCollection",
                                "statusCodes": []
                            },
                            {
                                "@id": "_:message_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Message entitity",
                                "expects": "vocab:Message",
                                "method": "PUT",
                                "returns": "vocab:Message",
                                "statusCodes": [
                                    {
                                        "description": "If the Message entity was created successfully.",
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
                    "hydra:description": "The DroneCollection collection",
                    "hydra:title": "dronecollection",
                    "property": {
                        "@id": "vocab:EntryPoint/DroneCollection",
                        "@type": "hydra:Link",
                        "description": "The DroneCollection collection",
                        "domain": "vocab:EntryPoint",
                        "label": "DroneCollection",
                        "range": "vocab:DroneCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:drone_collection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all Drone entities",
                                "expects": "null",
                                "method": "GET",
                                "returns": "vocab:DroneCollection",
                                "statusCodes": []
                            },
                            {
                                "@id": "_:drone_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Drone entitity",
                                "expects": "vocab:Drone",
                                "method": "PUT",
                                "returns": "vocab:Drone",
                                "statusCodes": [
                                    {
                                        "description": "If the Drone entity was created successfully.",
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
                    "hydra:description": "The LogEntryCollection collection",
                    "hydra:title": "logentrycollection",
                    "property": {
                        "@id": "vocab:EntryPoint/LogEntryCollection",
                        "@type": "hydra:Link",
                        "description": "The LogEntryCollection collection",
                        "domain": "vocab:EntryPoint",
                        "label": "LogEntryCollection",
                        "range": "vocab:LogEntryCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:logentry_collection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all LogEntry entities",
                                "expects": "null",
                                "method": "GET",
                                "returns": "vocab:LogEntryCollection",
                                "statusCodes": []
                            },
                            {
                                "@id": "_:logentry_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new LogEntry entitity",
                                "expects": "vocab:LogEntry",
                                "method": "PUT",
                                "returns": "vocab:LogEntry",
                                "statusCodes": [
                                    {
                                        "description": "If the LogEntry entity was created successfully.",
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
                    "hydra:description": "The DatastreamCollection collection",
                    "hydra:title": "datastreamcollection",
                    "property": {
                        "@id": "vocab:EntryPoint/DatastreamCollection",
                        "@type": "hydra:Link",
                        "description": "The DatastreamCollection collection",
                        "domain": "vocab:EntryPoint",
                        "label": "DatastreamCollection",
                        "range": "vocab:DatastreamCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:datastream_collection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all Datastream entities",
                                "expects": "null",
                                "method": "GET",
                                "returns": "vocab:DatastreamCollection",
                                "statusCodes": []
                            },
                            {
                                "@id": "_:datastream_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Datastream entitity",
                                "expects": "vocab:Datastream",
                                "method": "PUT",
                                "returns": "vocab:Datastream",
                                "statusCodes": [
                                    {
                                        "description": "If the Datastream entity was created successfully.",
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
    "title": "API Doc for the server side API"
}
