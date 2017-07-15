"""Generated API Documentation for Server API using server_doc_gen.py."""

server_doc = {
    "@context": {
        "ApiDocumentation": "hydra:ApiDocumentation",
        "code": "hydra:statusCode",
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
        "subClassOf": {
            "@id": "rdfs:subClassOf",
            "@type": "@id"
        },
        "supportedClass": "hydra:supportedClass",
        "supportedOperation": "hydra:supportedOperation",
        "supportedProperty": "hydra:supportedProperty",
        "title": "hydra:title",
        "vocab": "http://hydrus.com/serverapi/vocab#",
        "writeonly": "hydra:writeonly"
    },
    "@id": "http://hydrus.com/serverapi/vocab",
    "@type": "ApiDocumentation",
    "description": "API Documentation for the server side system",
    "entrypoint": "/serverapi",
    "possibleStatus": [],
    "supportedClass": [
        {
            "@id": "vocab:Status",
            "@type": "hydra:Class",
            "description": "Class for drone status objects",
            "supportedOperation": [],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://auto.schema.org/speed",
                    "readable": "true",
                    "required": "false",
                    "title": "Speed",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readable": "true",
                    "required": "false",
                    "title": "Position",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/fuelCapacity",
                    "readable": "true",
                    "required": "false",
                    "title": "Battery",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "https://schema.org/status",
                    "readable": "true",
                    "required": "false",
                    "title": "SensorStatus",
                    "writeable": "false"
                }
            ],
            "title": "Status"
        },
        {
            "@id": "vocab:Area",
            "@type": "hydra:Class",
            "description": "Class for Area of Interest of the server",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "expects": "http://hydrus.com/Area",
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
                            "description": "Area of not found",
                            "statusCode": 404
                        },
                        {
                            "description": "Area of returned",
                            "statusCode": 200
                        }
                    ],
                    "returns": "http://hydrus.com/Area",
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
            "@id": "vocab:Message",
            "@type": "hydra:Class",
            "description": "Class for messages received by the GUI interface",
            "supportedOperation": [],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/Text",
                    "readable": "true",
                    "required": "false",
                    "title": "MessageString",
                    "writeable": "true"
                }
            ],
            "title": "Message"
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
                    "readable": "false",
                    "required": "false",
                    "title": "Update",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:Status",
                    "readable": "false",
                    "required": "false",
                    "title": "Status",
                    "writeable": "false"
                }
            ],
            "title": "Command"
        },
        {
            "@id": "vocab:Drone",
            "@type": "hydra:Class",
            "description": "Class for a drone",
            "supportedOperation": [
                {
                    "@type": "hydra:Operation",
                    "expects": "vocab:Status",
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "description": "Drone Status updated",
                            "statusCode": 200
                        }
                    ],
                    "returns": "null",
                    "title": "SubmitStatus"
                },
                {
                    "@type": "hydra:Operation",
                    "expects": "null",
                    "method": "GET",
                    "possibleStatus": [
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
                    "property": "vocab:Status",
                    "readable": "true",
                    "required": "false",
                    "title": "DroneStatus",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/name",
                    "readable": "true",
                    "required": "false",
                    "title": "name",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/model",
                    "readable": "true",
                    "required": "false",
                    "title": "model",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://auto.schema.org/speed",
                    "readable": "true",
                    "required": "false",
                    "title": "MaxSpeed",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/device",
                    "readable": "true",
                    "required": "false",
                    "title": "Sensor",
                    "writeable": "true"
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
                    "title": "ReadData"
                },
                {
                    "@type": "hydra:Operation",
                    "expects": "vocab:Data",
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "description": "Data added",
                            "statusCode": 201
                        }
                    ],
                    "returns": "null",
                    "title": "SubmitData"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/QuantitativeValue",
                    "readable": "true",
                    "required": "false",
                    "title": "Temperature",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/identifier",
                    "readable": "true",
                    "required": "false",
                    "title": "DroneID",
                    "writeable": "false"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/geo",
                    "readable": "true",
                    "required": "false",
                    "title": "Position",
                    "writeable": "false"
                }
            ],
            "title": "Data"
        },
        {
            "@id": "vocab:LogEntry",
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
                    "returns": "voab:LogEntry",
                    "title": "GetLog"
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
                    "property": "vocab:Status",
                    "readable": "false",
                    "required": "false",
                    "title": "Status",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "vocab:Data",
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
                    "readable": "false",
                    "required": "null",
                    "title": "members",
                    "writeable": "false"
                }
            ],
            "title": "Collection"
        },
        {
            "@id": "vocab:LogEntryCollection",
            "@type": "hydra:Class",
            "description": "A collection of logentry",
            "label": "LogEntryCollection",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:logentry_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "null",
                    "expects": "LogEntry",
                    "method": "POST",
                    "returns": "LogEntry",
                    "statusCodes": [
                        {
                            "code": 201,
                            "description": "If the LogEntry entity was created successfully."
                        }
                    ]
                },
                {
                    "@id": "_:logentry_collection_retrieve",
                    "@type": "hydra:Operation",
                    "description": "null",
                    "expects": "null",
                    "label": "Retrieves all LogEntry entities",
                    "method": "GET",
                    "returns": "vocab:LogEntryCollection",
                    "statusCodes": []
                }
            ],
            "supportedProperty": [
                {
                    "hydra:description": "The logentry",
                    "hydra:title": "members",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "null",
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
                    "@id": "_:drone_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "null",
                    "expects": "Drone",
                    "method": "POST",
                    "returns": "Drone",
                    "statusCodes": [
                        {
                            "code": 201,
                            "description": "If the Drone entity was created successfully."
                        }
                    ]
                },
                {
                    "@id": "_:drone_collection_retrieve",
                    "@type": "hydra:Operation",
                    "description": "null",
                    "expects": "null",
                    "label": "Retrieves all Drone entities",
                    "method": "GET",
                    "returns": "vocab:DroneCollection",
                    "statusCodes": []
                }
            ],
            "supportedProperty": [
                {
                    "hydra:description": "The drone",
                    "hydra:title": "members",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "null",
                    "writeonly": "false"
                }
            ]
        },
        {
            "@id": "vocab:MessageCollection",
            "@type": "hydra:Class",
            "description": "A collection of message",
            "label": "MessageCollection",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:message_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "null",
                    "expects": "Message",
                    "method": "POST",
                    "returns": "Message",
                    "statusCodes": [
                        {
                            "code": 201,
                            "description": "If the Message entity was created successfully."
                        }
                    ]
                },
                {
                    "@id": "_:message_collection_retrieve",
                    "@type": "hydra:Operation",
                    "description": "null",
                    "expects": "null",
                    "label": "Retrieves all Message entities",
                    "method": "GET",
                    "returns": "vocab:MessageCollection",
                    "statusCodes": []
                }
            ],
            "supportedProperty": [
                {
                    "hydra:description": "The message",
                    "hydra:title": "members",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "null",
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
                    "@id": "_:data_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "null",
                    "expects": "Data",
                    "method": "POST",
                    "returns": "Data",
                    "statusCodes": [
                        {
                            "code": 201,
                            "description": "If the Data entity was created successfully."
                        }
                    ]
                },
                {
                    "@id": "_:data_collection_retrieve",
                    "@type": "hydra:Operation",
                    "description": "null",
                    "expects": "null",
                    "label": "Retrieves all Data entities",
                    "method": "GET",
                    "returns": "vocab:DataCollection",
                    "statusCodes": []
                }
            ],
            "supportedProperty": [
                {
                    "hydra:description": "The data",
                    "hydra:title": "members",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readonly": "false",
                    "required": "null",
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
                    "description": "null",
                    "expects": "null",
                    "label": "The APIs main entry point.",
                    "method": "GET",
                    "returns": "vocab:EntryPoint",
                    "statusCodes": []
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
                        "range": "vocab:AreaCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:updatearea",
                                "@type": "hydra:Operation",
                                "description": "null",
                                "expects": "http://hydrus.com/Area",
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
                                "returns": "http://hydrus.com/Area",
                                "statusCodes": [
                                    {
                                        "description": "Area of not found",
                                        "statusCode": 404
                                    },
                                    {
                                        "description": "Area of returned",
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
                    "hydra:description": "The Drone Class",
                    "hydra:title": "drone",
                    "property": {
                        "@id": "vocab:EntryPoint/Drone",
                        "@type": "hydra:Link",
                        "description": "Class for a drone",
                        "domain": "vocab:EntryPoint",
                        "label": "Drone",
                        "range": "vocab:DroneCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:submitstatus",
                                "@type": "hydra:Operation",
                                "description": "null",
                                "expects": "vocab:Status",
                                "label": "SubmitStatus",
                                "method": "PUT",
                                "returns": "null",
                                "statusCodes": [
                                    {
                                        "description": "Drone Status updated",
                                        "statusCode": 200
                                    }
                                ]
                            },
                            {
                                "@id": "_:getdrone",
                                "@type": "hydra:Operation",
                                "description": "null",
                                "expects": "null",
                                "label": "GetDrone",
                                "method": "GET",
                                "returns": "vocab:Drone",
                                "statusCodes": [
                                    {
                                        "description": "Drone Returned",
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
                    "hydra:description": "The LogEntryCollection collection",
                    "hydra:title": "logentrycollection",
                    "property": {
                        "@id": "vocab:EntryPoint/LogEntryCollection",
                        "@type": "hydra:Link",
                        "description": "The LogEntryCollection collection",
                        "domain": "vocab:EntryPoint",
                        "label": "LogEntryCollection",
                        "range": "vocab:LogEntryCollectionCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:logentrycollection_collection_retrieve",
                                "@type": "hydra:Operation",
                                "description": "null",
                                "expects": "null",
                                "label": "Retrieves all LogEntryCollection entities",
                                "method": "GET",
                                "returns": "vocab:LogEntryCollectionCollection",
                                "statusCodes": []
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
                        "range": "vocab:DroneCollectionCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:dronecollection_collection_retrieve",
                                "@type": "hydra:Operation",
                                "description": "null",
                                "expects": "null",
                                "label": "Retrieves all DroneCollection entities",
                                "method": "GET",
                                "returns": "vocab:DroneCollectionCollection",
                                "statusCodes": []
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
                        "range": "vocab:MessageCollectionCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:messagecollection_collection_retrieve",
                                "@type": "hydra:Operation",
                                "description": "null",
                                "expects": "null",
                                "label": "Retrieves all MessageCollection entities",
                                "method": "GET",
                                "returns": "vocab:MessageCollectionCollection",
                                "statusCodes": []
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
                        "range": "vocab:DataCollectionCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:datacollection_collection_retrieve",
                                "@type": "hydra:Operation",
                                "description": "null",
                                "expects": "null",
                                "label": "Retrieves all DataCollection entities",
                                "method": "GET",
                                "returns": "vocab:DataCollectionCollection",
                                "statusCodes": []
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
