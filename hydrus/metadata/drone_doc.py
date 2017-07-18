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
                            "description": "State Returned",
                            "statusCode": 200
                        }
                    ],
                    "returns": "vocab:State",
                    "title": "GetState"
                },
                {
                    "@type": "hydra:Operation",
                    "expects": "vocab:Command",
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "description": "Command issued",
                            "statusCode": 200
                        }
                    ],
                    "returns": "null",
                    "title": "IssueCommand"
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
            "@id": "vocab:State",
            "@type": "hydra:Class",
            "description": "Class for drone status objects",
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
            "@id": "vocab:StateCollection",
            "@type": "hydra:Class",
            "description": "A collection of state",
            "label": "StateCollection",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:state_collection_retrieve",
                    "@type": "hydra:Operation",
                    "expects": "null",
                    "label": "Retrieves all State entities",
                    "method": "GET",
                    "returns": "vocab:StateCollection",
                    "statusCodes": []
                },
                {
                    "@id": "_:state_create",
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:State",
                    "label": "Create new State entitity",
                    "method": "POST",
                    "returns": "vocab:State",
                    "statusCodes": [
                        {
                            "code": 201,
                            "description": "If the State entity was created successfully."
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
                    "expects": "null",
                    "label": "Retrieves all Data entities",
                    "method": "GET",
                    "returns": "vocab:DataCollection",
                    "statusCodes": []
                },
                {
                    "@id": "_:data_create",
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:Data",
                    "label": "Create new Data entitity",
                    "method": "POST",
                    "returns": "vocab:Data",
                    "statusCodes": [
                        {
                            "code": 201,
                            "description": "If the Data entity was created successfully."
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
            "@id": "vocab:DroneCollection",
            "@type": "hydra:Class",
            "description": "A collection of drone",
            "label": "DroneCollection",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:drone_collection_retrieve",
                    "@type": "hydra:Operation",
                    "expects": "null",
                    "label": "Retrieves all Drone entities",
                    "method": "GET",
                    "returns": "vocab:DroneCollection",
                    "statusCodes": []
                },
                {
                    "@id": "_:drone_create",
                    "@type": "http://schema.org/AddAction",
                    "expects": "vocab:Drone",
                    "label": "Create new Drone entitity",
                    "method": "POST",
                    "returns": "vocab:Drone",
                    "statusCodes": [
                        {
                            "code": 201,
                            "description": "If the Drone entity was created successfully."
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
                                        "description": "State Returned",
                                        "statusCode": 200
                                    }
                                ]
                            },
                            {
                                "@id": "_:issuecommand",
                                "@type": "hydra:Operation",
                                "description": "null",
                                "expects": "vocab:Command",
                                "label": "IssueCommand",
                                "method": "POST",
                                "returns": "null",
                                "statusCodes": [
                                    {
                                        "description": "Command issued",
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
                        "range": "vocab:StateCollection"
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
                        "range": "vocab:DataCollection"
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
                        "range": "vocab:DroneCollection"
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
