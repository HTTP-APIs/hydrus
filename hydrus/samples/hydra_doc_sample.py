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
        "readable": "hydra:readable",
        "required": "hydra:required",
        "returns": {
            "@id": "hydra:returns",
            "@type": "@id"
        },
        "statusCode": "hydra:statusCode",
        "subClassOf": {
            "@id": "rdfs:subClassOf",
            "@type": "@id"
        },
        "supportedClass": "hydra:supportedClass",
        "supportedOperation": "hydra:supportedOperation",
        "supportedProperty": "hydra:supportedProperty",
        "title": "hydra:title",
        "vocab": "http://localhost:8080/api/vocab#",
        "writeable": "hydra:writeable",
        "expectsHeader": "hydra:expectsHeader",
        "returnsHeader": "hydra:returnsHeader",
        "manages": "hydra:manages"
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
                            "title": "State not found",
                            "statusCode": 404,
                            "description": ""
                        },
                        {
                            "title": "State Returned",
                            "statusCode": 200,
                            "description": ""
                        }
                    ],
                    "returns": "vocab:State",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "GetState"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://auto.schema.org/speed",
                    "readable": "ture",
                    "required": "true",
                    "title": "Speed",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readable": "true",
                    "required": "true",
                    "title": "Position",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/Property",
                    "readable": "true",
                    "required": "true",
                    "title": "Direction",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/fuelCapacity",
                    "readable": "true",
                    "required": "true",
                    "title": "Battery",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/status",
                    "readable": "true",
                    "required": "true",
                    "title": "SensorStatus",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/identifier",
                    "readable": "true",
                    "required": "true",
                    "title": "DroneID",
                    "writeable": "true"
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
                            "title": "Command not found",
                            "statusCode": 404,
                            "description": ""
                        },
                        {
                            "title": "Command Returned",
                            "statusCode": 200,
                            "description": ""
                        }
                    ],
                    "returns": "vocab:Command",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "GetCommand"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:Command",
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "title": "Command added",
                            "statusCode": 201,
                            "description": ""
                        }
                    ],
                    "returns": "null",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "AddCommand"
                },
                {
                    "@type": "http://schema.org/DeleteAction",
                    "expects": "null",
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "title": "Command deleted",
                            "statusCode": 201,
                            "description": ""
                        }
                    ],
                    "returns": "null",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "DeleteCommand"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/identifier",
                    "readable": "true",
                    "required": "true",
                    "title": "DroneID",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:State",
                    "readable": "true",
                    "required": "true",
                    "title": "State",
                    "writeable": "true"
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
                            "title": "Message not found",
                            "statusCode": 404,
                            "description": ""
                        },
                        {
                            "title": "Message returned",
                            "statusCode": 200,
                            "description": ""
                        }
                    ],
                    "returns": "vocab:Message",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "GetMessage"
                },
                {
                    "@type": "http://schema.org/DeleteAction",
                    "expects": "null",
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "title": "Message deleted",
                            "statusCode": 200,
                            "description": ""
                        }
                    ],
                    "returns": "null",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "DeleteMessage"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/Text",
                    "readable": "true",
                    "required": "true",
                    "title": "MessageString",
                    "writeable": "true"
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
                            "title": "Area of interest changed",
                            "statusCode": 200,
                            "description": ""
                        }
                    ],
                    "returns": "null",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "UpdateArea"
                },
                {
                    "@type": "http://schema.org/FindAction",
                    "expects": "null",
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "title": "Area of interest not found",
                            "statusCode": 404,
                            "description": ""
                        },
                        {
                            "title": "Area of interest returned",
                            "statusCode": 200,
                            "description": ""
                        }
                    ],
                    "returns": "vocab:Area",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "GetArea"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readable": "true",
                    "required": "true",
                    "title": "TopLeft",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readable": "true",
                    "required": "true",
                    "title": "BottomRight",
                    "writeable": "true"
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
                            "title": "Data not found",
                            "statusCode": 404,
                            "description": ""
                        },
                        {
                            "title": "Data returned",
                            "statusCode": 200,
                            "description": ""
                        }
                    ],
                    "returns": "vocab:Datastream",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "ReadDatastream"
                },
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "vocab:Datastream",
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "title": "Data updated",
                            "statusCode": 200,
                            "description": ""
                        }
                    ],
                    "returns": "null",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "UpdateDatastream"
                },
                {
                    "@type": "http://schema.org/DeleteAction",
                    "expects": "null",
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "title": "Data deleted",
                            "statusCode": 200,
                            "description": ""
                        }
                    ],
                    "returns": "null",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "DeleteDatastream"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/QuantitativeValue",
                    "readable": "true",
                    "required": "true",
                    "title": "Temperature",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/identifier",
                    "readable": "true",
                    "required": "true",
                    "title": "DroneID",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readable": "true",
                    "required": "true",
                    "title": "Position",
                    "writeable": "true"
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
                            "title": "Drone updated",
                            "statusCode": 200,
                            "description": ""
                        }
                    ],
                    "returns": "null",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "SubmitDrone"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:Drone",
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "title": "Drone added",
                            "statusCode": 200,
                            "description": ""
                        }
                    ],
                    "returns": "null",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "CreateDrone"
                },
                {
                    "@type": "http://schema.org/FindAction",
                    "expects": "null",
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "title": "Drone not found",
                            "statusCode": 404,
                            "description": ""
                        },
                        {
                            "title": "Drone Returned",
                            "statusCode": 200,
                            "description": ""
                        }
                    ],
                    "returns": "vocab:Drone",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "GetDrone"
                },
                {
                    "@type": "http://schema.org/DeleteAction",
                    "expects": "null",
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "title": "Drone not found",
                            "statusCode": 404,
                            "description": ""
                        },
                        {
                            "title": "Drone successfully deleted",
                            "statusCode": 200,
                            "description": ""
                        }
                    ],
                    "returns": "null",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "DeleteDrone"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": {
                        "@id": "vocab:Drone/DroneState",
                        "@type": "hydra:Link",
                        "description": "",
                        "domain": "vocab:Drone",
                        "range": "vocab:State",
                        "supportedOperation": [],
                        "title": "Drone State"
                    },
                    "readable": "true",
                    "required": "false",
                    "title": "DroneState",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/name",
                    "readable": "true",
                    "required": "true",
                    "title": "name",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/model",
                    "readable": "true",
                    "required": "true",
                    "title": "model",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://auto.schema.org/speed",
                    "readable": "true",
                    "required": "true",
                    "title": "MaxSpeed",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/device",
                    "readable": "true",
                    "required": "true",
                    "title": "Sensor",
                    "writeable": "true"
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
                            "title": "Log entry not found",
                            "statusCode": 404,
                            "description": ""
                        },
                        {
                            "title": "Log entry returned",
                            "statusCode": 200,
                            "description": ""
                        }
                    ],
                    "returns": "vocab:LogEntry",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "GetLog"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:LogEntry",
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "title": "Log entry created",
                            "statusCode": 201,
                            "description": ""
                        }
                    ],
                    "returns": "null",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "title": "AddLog"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/identifier",
                    "readable": "true",
                    "required": "false",
                    "title": "DroneID",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/UpdateAction",
                    "readable": "false",
                    "required": "false",
                    "title": "Update",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/ReplyAction",
                    "readable": "false",
                    "required": "false",
                    "title": "Get",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/SendAction",
                    "readable": "false",
                    "required": "false",
                    "title": "Send",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:State",
                    "readable": "false",
                    "required": "false",
                    "title": "State",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:Datastream",
                    "readable": "false",
                    "required": "false",
                    "title": "Data",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:Command",
                    "readable": "false",
                    "required": "false",
                    "title": "Command",
                    "writeable": "true"
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
                    "readable": "true",
                    "required": "null",
                    "title": "members",
                    "writeable": "true"
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
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "possibleStatus": []
                },
                {
                    "@id": "_:command_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new Command entity",
                    "expects": "vocab:Command",
                    "method": "PUT",
                    "returns": "vocab:Command",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "possibleStatus": [
                        {
                            "title": "If the Command entity was created successfully.",
                            "statusCode": 201,
                            "description": ""
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The command",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "true",
                    "required": "false",
                    "title": "members",
                    "writeable": "true"
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
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "possibleStatus": []
                },
                {
                    "@id": "_:state_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new State entity",
                    "expects": "vocab:State",
                    "method": "PUT",
                    "returns": "vocab:State",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "possibleStatus": [
                        {
                            "title": "If the State entity was created successfully.",
                            "statusCode": 201,
                            "description": ""
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The state",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "true",
                    "required": "false",
                    "title": "members",
                    "writeable": "true"
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
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "possibleStatus": []
                },
                {
                    "@id": "_:message_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new Message entity",
                    "expects": "vocab:Message",
                    "method": "PUT",
                    "returns": "vocab:Message",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "possibleStatus": [
                        {
                            "title": "If the Message entity was created successfully.",
                            "statusCode": 201,
                            "description": ""
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The message",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "true",
                    "required": "false",
                    "title": "members",
                    "writeable": "true"
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
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "possibleStatus": []
                },
                {
                    "@id": "_:drone_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new Drone entity",
                    "expects": "vocab:Drone",
                    "method": "PUT",
                    "returns": "vocab:Drone",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "possibleStatus": [
                        {
                            "title": "If the Drone entity was created successfully.",
                            "statusCode": 201,
                            "description": ""
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The drone",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "true",
                    "required": "false",
                    "title": "members",
                    "writeable": "true"
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
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "possibleStatus": []
                },
                {
                    "@id": "_:logentry_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new LogEntry entity",
                    "expects": "vocab:LogEntry",
                    "method": "PUT",
                    "returns": "vocab:LogEntry",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "possibleStatus": [
                        {
                            "title": "If the LogEntry entity was created successfully.",
                            "statusCode": 201,
                            "description": ""
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The logentry",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "true",
                    "required": "false",
                    "title": "members",
                    "writeable": "true"
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
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "possibleStatus": []
                },
                {
                    "@id": "_:datastream_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new Datastream entity",
                    "expects": "vocab:Datastream",
                    "method": "PUT",
                    "returns": "vocab:Datastream",
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "possibleStatus": [
                        {
                            "title": "If the Datastream entity was created successfully.",
                            "statusCode": 201,
                            "description": ""
                        }
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The datastream",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "true",
                    "required": "false",
                    "title": "members",
                    "writeable": "true"
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
                    "expectsHeader": [],
                    "returnsHeader": [],
                    "possibleStatus": "vocab:EntryPoint"
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
                                "expectsHeader": [],
                                "returnsHeader": [],
                                "possibleStatus": [
                                    {
                                        "title": "Area of interest changed",
                                        "statusCode": 200,
                                        "description": ""
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
                                "expectsHeader": [],
                                "returnsHeader": [],
                                "possibleStatus": [
                                    {
                                        "title": "Area of interest not found",
                                        "statusCode": 404,
                                        "description": ""
                                    },
                                    {
                                        "title": "Area of interest returned",
                                        "statusCode": 200,
                                        "description": ""
                                    }
                                ]
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
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
                                "expectsHeader": [],
                                "returnsHeader": [],
                                "possibleStatus": []
                            },
                            {
                                "@id": "_:command_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Command entity",
                                "expects": "vocab:Command",
                                "method": "PUT",
                                "returns": "vocab:Command",
                                "expectsHeader": [],
                                "returnsHeader": [],
                                "possibleStatus": [
                                    {
                                        "title": "If the Command entity was created successfully.",
                                        "statusCode": 201,
                                        "description": ""
                                    }
                                ]
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
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
                                "expectsHeader": [],
                                "returnsHeader": [],
                                "possibleStatus": []
                            },
                            {
                                "@id": "_:state_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new State entity",
                                "expects": "vocab:State",
                                "method": "PUT",
                                "returns": "vocab:State",
                                "expectsHeader": [],
                                "returnsHeader": [],
                                "possibleStatus": [
                                    {
                                        "title": "If the State entity was created successfully.",
                                        "statusCode": 201,
                                        "description": ""
                                    }
                                ]
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
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
                                "expectsHeader": [],
                                "returnsHeader": [],
                                "possibleStatus": []
                            },
                            {
                                "@id": "_:message_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Message entity",
                                "expects": "vocab:Message",
                                "method": "PUT",
                                "returns": "vocab:Message",
                                "expectsHeader": [],
                                "returnsHeader": [],
                                "possibleStatus": [
                                    {
                                        "title": "If the Message entity was created successfully.",
                                        "statusCode": 201,
                                        "description": ""
                                    }
                                ]
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
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
                                "expectsHeader": [],
                                "returnsHeader": [],
                                "possibleStatus": []
                            },
                            {
                                "@id": "_:drone_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Drone entity",
                                "expects": "vocab:Drone",
                                "method": "PUT",
                                "returns": "vocab:Drone",
                                "expectsHeader": [],
                                "returnsHeader": [],
                                "possibleStatus": [
                                    {
                                        "title": "If the Drone entity was created successfully.",
                                        "statusCode": 201,
                                        "description": ""
                                    }
                                ]
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
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
                                "expectsHeader": [],
                                "returnsHeader": [],
                                "possibleStatus": []
                            },
                            {
                                "@id": "_:logentry_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new LogEntry entity",
                                "expects": "vocab:LogEntry",
                                "method": "PUT",
                                "returns": "vocab:LogEntry",
                                "expectsHeader": [],
                                "returnsHeader": [],
                                "possibleStatus": [
                                    {
                                        "title": "If the LogEntry entity was created successfully.",
                                        "statusCode": 201,
                                        "description": ""
                                    }
                                ]
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
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
                                "expectsHeader": [],
                                "returnsHeader": [],
                                "possibleStatus": []
                            },
                            {
                                "@id": "_:datastream_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Datastream entitity",
                                "expects": "vocab:Datastream",
                                "method": "PUT",
                                "returns": "vocab:Datastream",
                                "expectsHeader": [],
                                "returnsHeader": [],
                                "possibleStatus": [
                                    {
                                        "title": "If the Datastream entity was created successfully.",
                                        "statusCode": 201,
                                        "description": ""
                                    }
                                ]
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
    "title": "API Doc for the server side API"
}
