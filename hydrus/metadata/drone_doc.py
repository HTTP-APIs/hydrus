"""Generated API Documentation for Drone API using drone_doc_gen.py."""

drone_doc = {
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
        "vocab": "http://hydrus.com/droneapi/vocab#",
        "writeonly": "hydra:writeonly"
    },
    "@id": "http://hydrus.com/droneapi/vocab",
    "@type": "ApiDocumentation",
    "description": "API Documentation for the drone side system",
    "entrypoint": "/droneapi",
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
                            "description": "Status Returned",
                            "statusCode": 200
                        }
                    ],
                    "returns": "vocab:Status",
                    "title": "GetStatus"
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
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/identifier",
                    "readable": "true",
                    "required": "false",
                    "title": "DroneID",
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
                    "title": "GetData"
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
            "@id": "http://www.w3.org/ns/hydra/core#Resource",
            "@type": "hydra:Class",
            "description": "null",
            "supportedOperation": [],
            "supportedProperty": [],
            "title": "Resource"
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
                        "range": "vocab:DroneCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:getstatus",
                                "@type": "hydra:Operation",
                                "description": "null",
                                "expects": "null",
                                "label": "GetStatus",
                                "method": "GET",
                                "returns": "vocab:Status",
                                "statusCodes": [
                                    {
                                        "description": "Status Returned",
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
                        "range": "vocab:DataCollection",
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
                }
            ],
            "title": "EntryPoint"
        }
    ],
    "title": "API Doc for the drone side API"
}
