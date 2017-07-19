"""Generated API Documentation for Server API using server_doc_gen.py."""

server_doc = {
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
        "vocab": "http://localhost/serverapi/vocab#",
        "writeonly": "hydra:writeonly"
    },
    "@id": "http://localhost/serverapi/vocab",
    "@type": "ApiDocumentation",
    "description": "API Documentation for the server side system",
    "possibleStatus": [],
    "supportedClass": [
        {
            "@id": "vocab:vocab:Message",
            "@type": "hydra:Class",
            "description": "Class for messages received by the GUI interface",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
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
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/Text",
                    "readonly": "true",
                    "required": "false",
                    "title": "MessageString",
                    "writeonly": "true"
                }
            ],
            "title": "Message"
        },
        {
            "@id": "vocab:Drone",
            "@type": "hydra:Class",
            "description": "Class for a drone",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "expects": "vocab:State",
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "description": "Drone State updated",
                            "statusCode": 200
                        }
                    ],
                    "returns": "null",
                    "title": "SubmitState"
                },
                {
                    "@type": "hydra:Operation",
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
                }
            ],
            "title": "Drone"
        },
        {
            "@id": "vocab:vocab:Data",
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
                    "title": "ReadData"
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
            "@id": "vocab:vocab:LogEntry",
            "@type": "hydra:Class",
            "description": "Class for a log entry",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
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
                    "property": "vocab:Data",
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
            "@id": "vocab:Command",
            "@type": "hydra:Class",
            "description": "Class for drone commands",
            "supportedOperation": [],
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
            "@id": "vocab:vocab:Area",
            "@type": "hydra:Class",
            "description": "Class for Area of Interest of the server",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "expects": "vocab:Area",
                    "method": "PUT",
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
                    "@type": "hydra:Operation",
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
                    "readonly": "true",
                    "required": "true",
                    "title": "TopLeft",
                    "writeonly": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readonly": "true",
                    "required": "true",
                    "title": "BottomRight",
                    "writeonly": "true"
                }
            ],
            "title": "Area"
        },
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
            "@id": "vocab:MessageCollection",
            "@type": "hydra:Class",
            "description": "A collection of message",
            "label": "MessageCollection",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:message_collection_retrieve",
                    "@type": "hydra:Operation",
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
                    "expects": "vocab:vocab:Message",
                    "method": "PUT",
                    "returns": "vocab:vocab:Message",
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
            ]
        },
        {
            "@id": "vocab:DataCollection",
            "@type": "hydra:Class",
            "description": "A collection of data",
            "label": "DataCollection",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:data_collection_retrieve",
                    "@type": "hydra:Operation",
                    "description": "Retrieves all Data entities",
                    "expects": "null",
                    "method": "GET",
                    "returns": "vocab:DataCollection",
                    "statusCodes": []
                },
                {
                    "@id": "_:data_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new Data entitity",
                    "expects": "vocab:vocab:Data",
                    "method": "PUT",
                    "returns": "vocab:vocab:Data",
                    "statusCodes": [
                        {
                            "description": "If the Data entity was created successfully.",
                            "statusCode": 201
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The data",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "false",
                    "title": "members",
                    "writeonly": "false"
                }
            ]
        },
        {
            "@id": "vocab:LogEntryCollection",
            "@type": "hydra:Class",
            "description": "A collection of logentry",
            "label": "LogEntryCollection",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:logentry_collection_retrieve",
                    "@type": "hydra:Operation",
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
                    "expects": "vocab:vocab:LogEntry",
                    "method": "PUT",
                    "returns": "vocab:vocab:LogEntry",
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
            ]
        },
        {
            "@id": "vocab:DroneCollection",
            "@type": "hydra:Class",
            "description": "A collection of drone",
            "label": "DroneCollection",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:drone_collection_retrieve",
                    "@type": "hydra:Operation",
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
                    "hydra:description": "The Message Class",
                    "hydra:title": "message",
                    "property": {
                        "@id": "vocab:EntryPoint/Message",
                        "@type": "hydra:Link",
                        "description": "Class for messages received by the GUI interface",
                        "domain": "vocab:EntryPoint",
                        "label": "Message",
                        "range": "vocab:Message",
                        "supportedOperation": [
                            {
                                "@id": "_:getmessage",
                                "@type": "hydra:Operation",
                                "description": "null",
                                "expects": "null",
                                "label": "GetMessage",
                                "method": "GET",
                                "returns": "vocab:Message",
                                "statusCodes": [
                                    {
                                        "description": "Message not found",
                                        "statusCode": 404
                                    },
                                    {
                                        "description": "Message returned",
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
                                "@id": "_:updatearea",
                                "@type": "hydra:Operation",
                                "description": "null",
                                "expects": "vocab:Area",
                                "label": "UpdateArea",
                                "method": "PUT",
                                "returns": "null",
                                "statusCodes": [
                                    {
                                        "description": "Area of interest changed",
                                        "statusCode": 200
                                    }
                                ]
                            },
                            {
                                "@id": "_:getarea",
                                "@type": "hydra:Operation",
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
                                "@id": "_:_:message_collection_retrieve",
                                "@type": "hydra:Operation",
                                "description": "Retrieves all Message entities",
                                "expects": "null",
                                "method": "GET",
                                "returns": "vocab:MessageCollection",
                                "statusCodes": []
                            },
                            {
                                "@id": "_:_:message_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Message entitity",
                                "expects": "vocab:vocab:Message",
                                "method": "PUT",
                                "returns": "vocab:vocab:Message",
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
                    "hydra:description": "The DataCollection collection",
                    "hydra:title": "datacollection",
                    "property": {
                        "@id": "vocab:EntryPoint/DataCollection",
                        "@type": "hydra:Link",
                        "description": "The DataCollection collection",
                        "domain": "vocab:EntryPoint",
                        "label": "DataCollection",
                        "range": "vocab:DataCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:_:data_collection_retrieve",
                                "@type": "hydra:Operation",
                                "description": "Retrieves all Data entities",
                                "expects": "null",
                                "method": "GET",
                                "returns": "vocab:DataCollection",
                                "statusCodes": []
                            },
                            {
                                "@id": "_:_:data_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Data entitity",
                                "expects": "vocab:vocab:Data",
                                "method": "PUT",
                                "returns": "vocab:vocab:Data",
                                "statusCodes": [
                                    {
                                        "description": "If the Data entity was created successfully.",
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
                                "@id": "_:_:logentry_collection_retrieve",
                                "@type": "hydra:Operation",
                                "description": "Retrieves all LogEntry entities",
                                "expects": "null",
                                "method": "GET",
                                "returns": "vocab:LogEntryCollection",
                                "statusCodes": []
                            },
                            {
                                "@id": "_:_:logentry_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new LogEntry entitity",
                                "expects": "vocab:vocab:LogEntry",
                                "method": "PUT",
                                "returns": "vocab:vocab:LogEntry",
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
                                "@id": "_:_:drone_collection_retrieve",
                                "@type": "hydra:Operation",
                                "description": "Retrieves all Drone entities",
                                "expects": "null",
                                "method": "GET",
                                "returns": "vocab:DroneCollection",
                                "statusCodes": []
                            },
                            {
                                "@id": "_:_:drone_create",
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
                }
            ],
            "title": "EntryPoint"
        }
    ]
}