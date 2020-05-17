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
        "search": "hydra:search",
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
        "writeable": "hydra:writeable"
    },
    "@id": "http://localhost:8080/api/vocab",
    "@type": "ApiDocumentation",
    "description": "API Documentation for the server side system",
    "possibleStatus": [],
    "supportedClass": [
        {
            "@id": "vocab:Drone",
            "@type": "hydra:Class",
            "description": "Class for a drone",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "vocab:Drone",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Drone updated",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [],
                    "title": "SubmitDrone"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:Drone",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Drone added",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [],
                    "title": "CreateDrone"
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
                            "description": "Drone not found",
                            "statusCode": 404,
                            "title": ""
                        },
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Drone Returned",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "vocab:Drone",
                    "returnsHeader": [],
                    "title": "GetDrone"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:State",
                    "readable": "false",
                    "required": "true",
                    "title": "DroneState",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/name",
                    "readable": "false",
                    "required": "true",
                    "title": "name",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/model",
                    "readable": "false",
                    "required": "true",
                    "title": "model",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://auto.schema.org/speed",
                    "readable": "false",
                    "required": "true",
                    "title": "MaxSpeed",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/device",
                    "readable": "false",
                    "required": "true",
                    "title": "Sensor",
                    "writeable": "false"
                }
            ],
            "title": "Drone"
        },
        {
            "@id": "vocab:State",
            "@type": "hydra:Class",
            "description": "Class for drone state objects",
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
                            "description": "State not found",
                            "statusCode": 404,
                            "title": ""
                        },
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "State Returned",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "vocab:State",
                    "returnsHeader": [],
                    "title": "GetState"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://auto.schema.org/speed",
                    "readable": "false",
                    "required": "true",
                    "title": "Speed",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readable": "false",
                    "required": "true",
                    "title": "Position",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/Property",
                    "readable": "false",
                    "required": "true",
                    "title": "Direction",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/fuelCapacity",
                    "readable": "false",
                    "required": "true",
                    "title": "Battery",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/status",
                    "readable": "false",
                    "required": "true",
                    "title": "SensorStatus",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/identifier",
                    "readable": "false",
                    "required": "true",
                    "title": "DroneID",
                    "writeable": "false"
                }
            ],
            "title": "State"
        },
        {
            "@id": "vocab:Datastream",
            "@type": "hydra:Class",
            "description": "Class for a datastream entry",
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
                            "description": "Data not found",
                            "statusCode": 404,
                            "title": ""
                        },
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Data returned",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "vocab:Datastream",
                    "returnsHeader": [],
                    "title": "ReadDatastream"
                },
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "vocab:Datastream",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Data updated",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [],
                    "title": "UpdateDatastream"
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
                            "description": "Data deleted",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [],
                    "title": "DeleteDatastream"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/QuantitativeValue",
                    "readable": "false",
                    "required": "true",
                    "title": "Temperature",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/identifier",
                    "readable": "false",
                    "required": "true",
                    "title": "DroneID",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readable": "false",
                    "required": "true",
                    "title": "Position",
                    "writeable": "false"
                }
            ],
            "title": "Datastream"
        },
        {
            "@id": "vocab:LogEntry",
            "@type": "hydra:Class",
            "description": "Class for a log entry",
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
                            "description": "Log entry not found",
                            "statusCode": 404,
                            "title": ""
                        },
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Log entry returned",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "vocab:LogEntry",
                    "returnsHeader": [],
                    "title": "GetLog"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:LogEntry",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Log entry created",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "null",
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
            "@id": "vocab:Area",
            "@type": "hydra:Class",
            "description": "Class for Area of Interest of the server",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "vocab:Area",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Area of interest changed",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [],
                    "title": "UpdateArea"
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
                            "description": "Area of interest not found",
                            "statusCode": 200,
                            "title": ""
                        },
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Area of interest returned",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "vocab:Area",
                    "returnsHeader": [],
                    "title": "GetArea"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readable": "false",
                    "required": "true",
                    "title": "TopLeft",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readable": "false",
                    "required": "true",
                    "title": "BottomRight",
                    "writeable": "false"
                }
            ],
            "title": "Area"
        },
        {
            "@id": "vocab:Command",
            "@type": "hydra:Class",
            "description": "Class for drone commands",
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
                            "description": "Command not found",
                            "statusCode": 404,
                            "title": ""
                        },
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Command Returned",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "vocab:Command",
                    "returnsHeader": [],
                    "title": "GetCommand"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:Command",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Command added",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [],
                    "title": "AddCommand"
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
                            "description": "Command deleted",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [],
                    "title": "DeleteCommand"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/identifier",
                    "readable": "false",
                    "required": "true",
                    "title": "DroneID",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:State",
                    "readable": "false",
                    "required": "true",
                    "title": "State",
                    "writeable": "false"
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
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Message not found",
                            "statusCode": 200,
                            "title": ""
                        },
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Message returned",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "vocab:Message",
                    "returnsHeader": [],
                    "title": "GetMessage"
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
                            "description": "Message deleted",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [],
                    "title": "DeleteMessage"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/Text",
                    "readable": "false",
                    "required": "true",
                    "title": "MessageString",
                    "writeable": "false"
                }
            ],
            "title": "Message"
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
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "vocab:DroneCollection",
                    "returnsHeader": []
                },
                {
                    "@id": "_:drone_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new Drone entity",
                    "expects": "vocab:Drone",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "If the Drone entity was createdsuccessfully.",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "vocab:Drone",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The drone",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "false",
                    "required": "false",
                    "title": "members",
                    "writeable": "false"
                }
            ],
            "title": "DroneCollection"
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
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "vocab:StateCollection",
                    "returnsHeader": []
                },
                {
                    "@id": "_:state_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new State entity",
                    "expects": "vocab:State",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "If the State entity was createdsuccessfully.",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "vocab:State",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The state",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "false",
                    "required": "false",
                    "title": "members",
                    "writeable": "false"
                }
            ],
            "title": "StateCollection"
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
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "vocab:DatastreamCollection",
                    "returnsHeader": []
                },
                {
                    "@id": "_:datastream_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new Datastream entity",
                    "expects": "vocab:Datastream",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "If the Datastream entity was createdsuccessfully.",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "vocab:Datastream",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The datastream",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "false",
                    "required": "false",
                    "title": "members",
                    "writeable": "false"
                }
            ],
            "title": "DatastreamCollection"
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
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "vocab:LogEntryCollection",
                    "returnsHeader": []
                },
                {
                    "@id": "_:logentry_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new LogEntry entity",
                    "expects": "vocab:LogEntry",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "If the LogEntry entity was createdsuccessfully.",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "vocab:LogEntry",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The logentry",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "false",
                    "required": "false",
                    "title": "members",
                    "writeable": "false"
                }
            ],
            "title": "LogEntryCollection"
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
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "vocab:CommandCollection",
                    "returnsHeader": []
                },
                {
                    "@id": "_:command_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new Command entity",
                    "expects": "vocab:Command",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "If the Command entity was createdsuccessfully.",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "vocab:Command",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The command",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "false",
                    "required": "false",
                    "title": "members",
                    "writeable": "false"
                }
            ],
            "title": "CommandCollection"
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
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "vocab:MessageCollection",
                    "returnsHeader": []
                },
                {
                    "@id": "_:message_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new Message entity",
                    "expects": "vocab:Message",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "If the Message entity was createdsuccessfully.",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "vocab:Message",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The message",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "false",
                    "required": "false",
                    "title": "members",
                    "writeable": "false"
                }
            ],
            "title": "MessageCollection"
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
                                "expectsHeader": [],
                                "label": "UpdateArea",
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "Area of interest changed",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "null",
                                "returnsHeader": []
                            },
                            {
                                "@id": "getarea",
                                "@type": "http://schema.org/FindAction",
                                "description": "null",
                                "expects": "null",
                                "expectsHeader": [],
                                "label": "GetArea",
                                "method": "GET",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "Area of interest not found",
                                        "statusCode": 200,
                                        "title": ""
                                    },
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "Area of interest returned",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "vocab:Area",
                                "returnsHeader": []
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
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "vocab:DroneCollection",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:drone_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Drone entity",
                                "expects": "vocab:Drone",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "If the Drone entity was createdsuccessfully.",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "vocab:Drone",
                                "returnsHeader": []
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
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "vocab:StateCollection",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:state_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new State entity",
                                "expects": "vocab:State",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "If the State entity was createdsuccessfully.",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "vocab:State",
                                "returnsHeader": []
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
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "vocab:DatastreamCollection",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:datastream_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Datastream entity",
                                "expects": "vocab:Datastream",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "If the Datastream entity was createdsuccessfully.",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "vocab:Datastream",
                                "returnsHeader": []
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
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "vocab:LogEntryCollection",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:logentry_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new LogEntry entity",
                                "expects": "vocab:LogEntry",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "If the LogEntry entity was createdsuccessfully.",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "vocab:LogEntry",
                                "returnsHeader": []
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
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "vocab:CommandCollection",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:command_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Command entity",
                                "expects": "vocab:Command",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "If the Command entity was createdsuccessfully.",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "vocab:Command",
                                "returnsHeader": []
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
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "vocab:MessageCollection",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:message_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new Message entity",
                                "expects": "vocab:Message",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "If the Message entity was createdsuccessfully.",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "vocab:Message",
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
    "title": "API Doc for the server side API"
}