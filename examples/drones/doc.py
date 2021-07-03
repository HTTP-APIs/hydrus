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
        "entrypoint": {
            "@id": "hydra:entrypoint",
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
        "object": {
            "@id": "hydra:object",
            "@type": "@id"
        },
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
        "subject": {
            "@id": "hydra:subject",
            "@type": "@id"
        },
        "supportedClass": "hydra:supportedClass",
        "supportedOperation": "hydra:supportedOperation",
        "supportedProperty": "hydra:supportedProperty",
        "title": "hydra:title",
        "writeable": "hydra:writeable",
        "xsd": "https://www.w3.org/TR/xmlschema-2/#"
    },
    "@id": "http://localhost:8080/api/vocab",
    "@type": "ApiDocumentation",
    "description": "API Documentation for the server side system",
    "entrypoint": "http://localhost:8080/api",
    "possibleStatus": [],
    "supportedClass": [
        {
            "@id": "http://localhost:8080/api/vocab?resource=Drone",
            "@type": "hydra:Class",
            "description": "Class for a drone",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "http://localhost:8080/api/vocab?resource=Drone",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
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
                    "expects": "http://localhost:8080/api/vocab?resource=Drone",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
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
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "Drone not found",
                            "statusCode": 404,
                            "title": ""
                        },
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "Drone Returned",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Drone",
                    "returnsHeader": [],
                    "title": "GetDrone"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://localhost:8080/api/vocab?resource=State",
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
            "@id": "http://localhost:8080/api/vocab?resource=State",
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
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "State not found",
                            "statusCode": 404,
                            "title": ""
                        },
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "State Returned",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=State",
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
            "@id": "http://localhost:8080/api/vocab?resource=Datastream",
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
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "Data not found",
                            "statusCode": 404,
                            "title": ""
                        },
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "Data returned",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Datastream",
                    "returnsHeader": [],
                    "title": "ReadDatastream"
                },
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "http://localhost:8080/api/vocab?resource=Datastream",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
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
                            "@context": "https://www.w3.org/ns/hydra/core",
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
            "@id": "http://localhost:8080/api/vocab?resource=LogEntry",
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
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "Log entry not found",
                            "statusCode": 404,
                            "title": ""
                        },
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "Log entry returned",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=LogEntry",
                    "returnsHeader": [],
                    "title": "GetLog"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "http://localhost:8080/api/vocab?resource=LogEntry",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
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
                    "property": "http://localhost:8080/api/vocab?resource=State",
                    "readable": "false",
                    "required": "false",
                    "title": "State",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://localhost:8080/api/vocab?resource=Datastream",
                    "readable": "false",
                    "required": "false",
                    "title": "Data",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://localhost:8080/api/vocab?resource=Command",
                    "readable": "false",
                    "required": "false",
                    "title": "Command",
                    "writeable": "true"
                }
            ],
            "title": "LogEntry"
        },
        {
            "@id": "http://localhost:8080/api/vocab?resource=Area",
            "@type": "hydra:Class",
            "description": "Class for Area of Interest of the server",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "http://localhost:8080/api/vocab?resource=Area",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
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
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "Area of interest not found",
                            "statusCode": 200,
                            "title": ""
                        },
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "Area of interest returned",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Area",
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
            "@id": "http://localhost:8080/api/vocab?resource=Command",
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
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "Command not found",
                            "statusCode": 404,
                            "title": ""
                        },
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "Command Returned",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Command",
                    "returnsHeader": [],
                    "title": "GetCommand"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "http://localhost:8080/api/vocab?resource=Command",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
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
                            "@context": "https://www.w3.org/ns/hydra/core",
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
                    "property": "http://localhost:8080/api/vocab?resource=State",
                    "readable": "false",
                    "required": "true",
                    "title": "State",
                    "writeable": "false"
                }
            ],
            "title": "Command"
        },
        {
            "@id": "http://localhost:8080/api/vocab?resource=Message",
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
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "Message not found",
                            "statusCode": 200,
                            "title": ""
                        },
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "Message returned",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Message",
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
                            "@context": "https://www.w3.org/ns/hydra/core",
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
            "@id": "http://localhost:8080/api/vocab?resource=DroneCollection",
            "@type": "Collection",
            "description": "A collection of drones",
            "manages": {
                "object": "http://localhost:8080/api/vocab?resource=Drone",
                "property": "rdfs:type"
            },
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:DroneCollection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all the members of DroneCollection",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "http://localhost:8080/api/vocab?resource=Drone",
                    "returnsHeader": []
                },
                {
                    "@id": "_:DroneCollection_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new member in DroneCollection",
                    "expects": "http://localhost:8080/api/vocab?resource=Drone",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "A new member in DroneCollection created",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Drone",
                    "returnsHeader": []
                },
                {
                    "@id": "_:DroneCollection_update",
                    "@type": "http://schema.org/UpdateAction",
                    "description": "Update member of  DroneCollection ",
                    "expects": "http://localhost:8080/api/vocab?resource=Drone",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "If the entity was updatedfrom DroneCollection.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Drone",
                    "returnsHeader": []
                },
                {
                    "@id": "_:DroneCollection_delete",
                    "@type": "http://schema.org/DeleteAction",
                    "description": "Delete member of DroneCollection ",
                    "expects": "http://localhost:8080/api/vocab?resource=Drone",
                    "expectsHeader": [],
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "If entity was deletedsuccessfully from DroneCollection.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Drone",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The members of DroneCollection",
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
            "@id": "http://localhost:8080/api/vocab?resource=StateCollection",
            "@type": "Collection",
            "description": "A collection of states",
            "manages": {
                "object": "http://localhost:8080/api/vocab?resource=State",
                "property": "rdfs:type"
            },
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:StateCollection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all the members of StateCollection",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "http://localhost:8080/api/vocab?resource=State",
                    "returnsHeader": []
                },
                {
                    "@id": "_:StateCollection_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new member in StateCollection",
                    "expects": "http://localhost:8080/api/vocab?resource=State",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "A new member in StateCollection created",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=State",
                    "returnsHeader": []
                },
                {
                    "@id": "_:StateCollection_update",
                    "@type": "http://schema.org/UpdateAction",
                    "description": "Update member of  StateCollection ",
                    "expects": "http://localhost:8080/api/vocab?resource=State",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "If the entity was updatedfrom StateCollection.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=State",
                    "returnsHeader": []
                },
                {
                    "@id": "_:StateCollection_delete",
                    "@type": "http://schema.org/DeleteAction",
                    "description": "Delete member of StateCollection ",
                    "expects": "http://localhost:8080/api/vocab?resource=State",
                    "expectsHeader": [],
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "If entity was deletedsuccessfully from StateCollection.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=State",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The members of StateCollection",
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
            "@id": "http://localhost:8080/api/vocab?resource=DatastreamCollection",
            "@type": "Collection",
            "description": "A collection of datastream",
            "manages": {
                "object": "http://localhost:8080/api/vocab?resource=Datastream",
                "property": "rdfs:type"
            },
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:DatastreamCollection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all the members of DatastreamCollection",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "http://localhost:8080/api/vocab?resource=Datastream",
                    "returnsHeader": []
                },
                {
                    "@id": "_:DatastreamCollection_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new member in DatastreamCollection",
                    "expects": "http://localhost:8080/api/vocab?resource=Datastream",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "A new member in DatastreamCollection created",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Datastream",
                    "returnsHeader": []
                },
                {
                    "@id": "_:DatastreamCollection_update",
                    "@type": "http://schema.org/UpdateAction",
                    "description": "Update member of  DatastreamCollection ",
                    "expects": "http://localhost:8080/api/vocab?resource=Datastream",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "If the entity was updatedfrom DatastreamCollection.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Datastream",
                    "returnsHeader": []
                },
                {
                    "@id": "_:DatastreamCollection_delete",
                    "@type": "http://schema.org/DeleteAction",
                    "description": "Delete member of DatastreamCollection ",
                    "expects": "http://localhost:8080/api/vocab?resource=Datastream",
                    "expectsHeader": [],
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "If entity was deletedsuccessfully from DatastreamCollection.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Datastream",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The members of DatastreamCollection",
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
            "@id": "http://localhost:8080/api/vocab?resource=LogEntryCollection",
            "@type": "Collection",
            "description": "A collection of logs",
            "manages": {
                "object": "http://localhost:8080/api/vocab?resource=LogEntry",
                "property": "rdfs:type"
            },
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:LogEntryCollection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all the members of LogEntryCollection",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "http://localhost:8080/api/vocab?resource=LogEntry",
                    "returnsHeader": []
                },
                {
                    "@id": "_:LogEntryCollection_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new member in LogEntryCollection",
                    "expects": "http://localhost:8080/api/vocab?resource=LogEntry",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "A new member in LogEntryCollection created",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=LogEntry",
                    "returnsHeader": []
                },
                {
                    "@id": "_:LogEntryCollection_update",
                    "@type": "http://schema.org/UpdateAction",
                    "description": "Update member of  LogEntryCollection ",
                    "expects": "http://localhost:8080/api/vocab?resource=LogEntry",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "If the entity was updatedfrom LogEntryCollection.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=LogEntry",
                    "returnsHeader": []
                },
                {
                    "@id": "_:LogEntryCollection_delete",
                    "@type": "http://schema.org/DeleteAction",
                    "description": "Delete member of LogEntryCollection ",
                    "expects": "http://localhost:8080/api/vocab?resource=LogEntry",
                    "expectsHeader": [],
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "If entity was deletedsuccessfully from LogEntryCollection.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=LogEntry",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The members of LogEntryCollection",
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
            "@id": "http://localhost:8080/api/vocab?resource=CommandCollection",
            "@type": "Collection",
            "description": "A collection of commands",
            "manages": {
                "object": "http://localhost:8080/api/vocab?resource=Command",
                "property": "rdfs:type"
            },
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:CommandCollection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all the members of CommandCollection",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "http://localhost:8080/api/vocab?resource=Command",
                    "returnsHeader": []
                },
                {
                    "@id": "_:CommandCollection_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new member in CommandCollection",
                    "expects": "http://localhost:8080/api/vocab?resource=Command",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "A new member in CommandCollection created",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Command",
                    "returnsHeader": []
                },
                {
                    "@id": "_:CommandCollection_update",
                    "@type": "http://schema.org/UpdateAction",
                    "description": "Update member of  CommandCollection ",
                    "expects": "http://localhost:8080/api/vocab?resource=Command",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "If the entity was updatedfrom CommandCollection.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Command",
                    "returnsHeader": []
                },
                {
                    "@id": "_:CommandCollection_delete",
                    "@type": "http://schema.org/DeleteAction",
                    "description": "Delete member of CommandCollection ",
                    "expects": "http://localhost:8080/api/vocab?resource=Command",
                    "expectsHeader": [],
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "If entity was deletedsuccessfully from CommandCollection.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Command",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The members of CommandCollection",
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
            "@id": "http://localhost:8080/api/vocab?resource=MessageCollection",
            "@type": "Collection",
            "description": "A collection of messages",
            "manages": {
                "object": "http://localhost:8080/api/vocab?resource=Message",
                "property": "rdfs:type"
            },
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:MessageCollection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all the members of MessageCollection",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "http://localhost:8080/api/vocab?resource=Message",
                    "returnsHeader": []
                },
                {
                    "@id": "_:MessageCollection_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new member in MessageCollection",
                    "expects": "http://localhost:8080/api/vocab?resource=Message",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "A new member in MessageCollection created",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Message",
                    "returnsHeader": []
                },
                {
                    "@id": "_:MessageCollection_update",
                    "@type": "http://schema.org/UpdateAction",
                    "description": "Update member of  MessageCollection ",
                    "expects": "http://localhost:8080/api/vocab?resource=Message",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "If the entity was updatedfrom MessageCollection.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Message",
                    "returnsHeader": []
                },
                {
                    "@id": "_:MessageCollection_delete",
                    "@type": "http://schema.org/DeleteAction",
                    "description": "Delete member of MessageCollection ",
                    "expects": "http://localhost:8080/api/vocab?resource=Message",
                    "expectsHeader": [],
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "@context": "https://www.w3.org/ns/hydra/core",
                            "@type": "Status",
                            "description": "If entity was deletedsuccessfully from MessageCollection.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/api/vocab?resource=Message",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The members of MessageCollection",
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
            "@id": "http://localhost:8080/api#EntryPoint",
            "@type": "hydra:Class",
            "description": "The main entry point or homepage of the API.",
            "supportedOperation": [
                {
                    "@id": "_:entry_point",
                    "@type": "http://localhost:8080//api#EntryPoint",
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
                    "hydra:description": "The Drone Class",
                    "hydra:title": "drone",
                    "property": {
                        "@id": "http://localhost:8080/api/vocab?resource=EntryPoint/Drone",
                        "@type": "hydra:Link",
                        "description": "Class for a drone",
                        "domain": "http://localhost:8080/api/vocab?resource=EntryPoint",
                        "label": "Drone",
                        "range": "http://localhost:8080/api/vocab?resource=Drone",
                        "supportedOperation": [
                            {
                                "@id": "submitdrone",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "null",
                                "expects": "http://localhost:8080/api/vocab?resource=Drone",
                                "expectsHeader": [],
                                "label": "SubmitDrone",
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Drone updated",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "null",
                                "returnsHeader": []
                            },
                            {
                                "@id": "createdrone",
                                "@type": "http://schema.org/AddAction",
                                "description": "null",
                                "expects": "http://localhost:8080/api/vocab?resource=Drone",
                                "expectsHeader": [],
                                "label": "CreateDrone",
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Drone added",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "null",
                                "returnsHeader": []
                            },
                            {
                                "@id": "getdrone",
                                "@type": "http://schema.org/FindAction",
                                "description": "null",
                                "expects": "null",
                                "expectsHeader": [],
                                "label": "GetDrone",
                                "method": "GET",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Drone not found",
                                        "statusCode": 404,
                                        "title": ""
                                    },
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Drone Returned",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Drone",
                                "returnsHeader": []
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
                },
                {
                    "hydra:description": "The State Class",
                    "hydra:title": "state",
                    "property": {
                        "@id": "http://localhost:8080/api/vocab?resource=EntryPoint/State",
                        "@type": "hydra:Link",
                        "description": "Class for drone state objects",
                        "domain": "http://localhost:8080/api/vocab?resource=EntryPoint",
                        "label": "State",
                        "range": "http://localhost:8080/api/vocab?resource=State",
                        "supportedOperation": [
                            {
                                "@id": "getstate",
                                "@type": "http://schema.org/FindAction",
                                "description": "null",
                                "expects": "null",
                                "expectsHeader": [],
                                "label": "GetState",
                                "method": "GET",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "State not found",
                                        "statusCode": 404,
                                        "title": ""
                                    },
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "State Returned",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=State",
                                "returnsHeader": []
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
                },
                {
                    "hydra:description": "The Datastream Class",
                    "hydra:title": "datastream",
                    "property": {
                        "@id": "http://localhost:8080/api/vocab?resource=EntryPoint/Datastream",
                        "@type": "hydra:Link",
                        "description": "Class for a datastream entry",
                        "domain": "http://localhost:8080/api/vocab?resource=EntryPoint",
                        "label": "Datastream",
                        "range": "http://localhost:8080/api/vocab?resource=Datastream",
                        "supportedOperation": [
                            {
                                "@id": "readdatastream",
                                "@type": "http://schema.org/FindAction",
                                "description": "null",
                                "expects": "null",
                                "expectsHeader": [],
                                "label": "ReadDatastream",
                                "method": "GET",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Data not found",
                                        "statusCode": 404,
                                        "title": ""
                                    },
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Data returned",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Datastream",
                                "returnsHeader": []
                            },
                            {
                                "@id": "updatedatastream",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "null",
                                "expects": "http://localhost:8080/api/vocab?resource=Datastream",
                                "expectsHeader": [],
                                "label": "UpdateDatastream",
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Data updated",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "null",
                                "returnsHeader": []
                            },
                            {
                                "@id": "deletedatastream",
                                "@type": "http://schema.org/DeleteAction",
                                "description": "null",
                                "expects": "null",
                                "expectsHeader": [],
                                "label": "DeleteDatastream",
                                "method": "DELETE",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Data deleted",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "null",
                                "returnsHeader": []
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
                },
                {
                    "hydra:description": "The LogEntry Class",
                    "hydra:title": "logentry",
                    "property": {
                        "@id": "http://localhost:8080/api/vocab?resource=EntryPoint/LogEntry",
                        "@type": "hydra:Link",
                        "description": "Class for a log entry",
                        "domain": "http://localhost:8080/api/vocab?resource=EntryPoint",
                        "label": "LogEntry",
                        "range": "http://localhost:8080/api/vocab?resource=LogEntry",
                        "supportedOperation": [
                            {
                                "@id": "getlog",
                                "@type": "http://schema.org/FindAction",
                                "description": "null",
                                "expects": "null",
                                "expectsHeader": [],
                                "label": "GetLog",
                                "method": "GET",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Log entry not found",
                                        "statusCode": 404,
                                        "title": ""
                                    },
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Log entry returned",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=LogEntry",
                                "returnsHeader": []
                            },
                            {
                                "@id": "addlog",
                                "@type": "http://schema.org/AddAction",
                                "description": "null",
                                "expects": "http://localhost:8080/api/vocab?resource=LogEntry",
                                "expectsHeader": [],
                                "label": "AddLog",
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Log entry created",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "null",
                                "returnsHeader": []
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
                },
                {
                    "hydra:description": "The Area Class",
                    "hydra:title": "area",
                    "property": {
                        "@id": "http://localhost:8080/api/vocab?resource=EntryPoint/Area",
                        "@type": "hydra:Link",
                        "description": "Class for Area of Interest of the server",
                        "domain": "http://localhost:8080/api/vocab?resource=EntryPoint",
                        "label": "Area",
                        "range": "http://localhost:8080/api/vocab?resource=Area",
                        "supportedOperation": [
                            {
                                "@id": "updatearea",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "null",
                                "expects": "http://localhost:8080/api/vocab?resource=Area",
                                "expectsHeader": [],
                                "label": "UpdateArea",
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
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
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Area of interest not found",
                                        "statusCode": 200,
                                        "title": ""
                                    },
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Area of interest returned",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Area",
                                "returnsHeader": []
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
                },
                {
                    "hydra:description": "The Command Class",
                    "hydra:title": "command",
                    "property": {
                        "@id": "http://localhost:8080/api/vocab?resource=EntryPoint/Command",
                        "@type": "hydra:Link",
                        "description": "Class for drone commands",
                        "domain": "http://localhost:8080/api/vocab?resource=EntryPoint",
                        "label": "Command",
                        "range": "http://localhost:8080/api/vocab?resource=Command",
                        "supportedOperation": [
                            {
                                "@id": "getcommand",
                                "@type": "http://schema.org/FindAction",
                                "description": "null",
                                "expects": "null",
                                "expectsHeader": [],
                                "label": "GetCommand",
                                "method": "GET",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Command not found",
                                        "statusCode": 404,
                                        "title": ""
                                    },
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Command Returned",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Command",
                                "returnsHeader": []
                            },
                            {
                                "@id": "addcommand",
                                "@type": "http://schema.org/AddAction",
                                "description": "null",
                                "expects": "http://localhost:8080/api/vocab?resource=Command",
                                "expectsHeader": [],
                                "label": "AddCommand",
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Command added",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "null",
                                "returnsHeader": []
                            },
                            {
                                "@id": "deletecommand",
                                "@type": "http://schema.org/DeleteAction",
                                "description": "null",
                                "expects": "null",
                                "expectsHeader": [],
                                "label": "DeleteCommand",
                                "method": "DELETE",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Command deleted",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "null",
                                "returnsHeader": []
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
                },
                {
                    "hydra:description": "The Message Class",
                    "hydra:title": "message",
                    "property": {
                        "@id": "http://localhost:8080/api/vocab?resource=EntryPoint/Message",
                        "@type": "hydra:Link",
                        "description": "Class for messages received by the GUI interface",
                        "domain": "http://localhost:8080/api/vocab?resource=EntryPoint",
                        "label": "Message",
                        "range": "http://localhost:8080/api/vocab?resource=Message",
                        "supportedOperation": [
                            {
                                "@id": "getmessage",
                                "@type": "http://schema.org/FindAction",
                                "description": "null",
                                "expects": "null",
                                "expectsHeader": [],
                                "label": "GetMessage",
                                "method": "GET",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Message not found",
                                        "statusCode": 200,
                                        "title": ""
                                    },
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Message returned",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Message",
                                "returnsHeader": []
                            },
                            {
                                "@id": "deletemessage",
                                "@type": "http://schema.org/DeleteAction",
                                "description": "null",
                                "expects": "null",
                                "expectsHeader": [],
                                "label": "DeleteMessage",
                                "method": "DELETE",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "Message deleted",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "null",
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
                        "@id": "http://localhost:8080/api/vocab?resource=EntryPoint/DroneCollection",
                        "@type": "hydra:Link",
                        "description": "The DroneCollection collection",
                        "domain": "http://localhost:8080/api/vocab?resource=EntryPoint",
                        "label": "DroneCollection",
                        "manages": {
                            "object": "http://localhost:8080/api/vocab?resource=Drone",
                            "property": "rdfs:type"
                        },
                        "range": "http://localhost:8080/api/vocab?resource=DroneCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:dronecollection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all the members of DroneCollection",
                                "expects": "null",
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "http://localhost:8080/api/vocab?resource=Drone",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:dronecollection_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new member in DroneCollection",
                                "expects": "http://localhost:8080/api/vocab?resource=Drone",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "A new member in DroneCollection created",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Drone",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:dronecollection_update",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "Update member of  DroneCollection ",
                                "expects": "http://localhost:8080/api/vocab?resource=Drone",
                                "expectsHeader": [],
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "If the entity was updatedfrom DroneCollection.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Drone",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:dronecollection_delete",
                                "@type": "http://schema.org/DeleteAction",
                                "description": "Delete member of DroneCollection ",
                                "expects": "http://localhost:8080/api/vocab?resource=Drone",
                                "expectsHeader": [],
                                "method": "DELETE",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "If entity was deletedsuccessfully from DroneCollection.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Drone",
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
                        "@id": "http://localhost:8080/api/vocab?resource=EntryPoint/StateCollection",
                        "@type": "hydra:Link",
                        "description": "The StateCollection collection",
                        "domain": "http://localhost:8080/api/vocab?resource=EntryPoint",
                        "label": "StateCollection",
                        "manages": {
                            "object": "http://localhost:8080/api/vocab?resource=State",
                            "property": "rdfs:type"
                        },
                        "range": "http://localhost:8080/api/vocab?resource=StateCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:statecollection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all the members of StateCollection",
                                "expects": "null",
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "http://localhost:8080/api/vocab?resource=State",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:statecollection_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new member in StateCollection",
                                "expects": "http://localhost:8080/api/vocab?resource=State",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "A new member in StateCollection created",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=State",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:statecollection_update",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "Update member of  StateCollection ",
                                "expects": "http://localhost:8080/api/vocab?resource=State",
                                "expectsHeader": [],
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "If the entity was updatedfrom StateCollection.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=State",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:statecollection_delete",
                                "@type": "http://schema.org/DeleteAction",
                                "description": "Delete member of StateCollection ",
                                "expects": "http://localhost:8080/api/vocab?resource=State",
                                "expectsHeader": [],
                                "method": "DELETE",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "If entity was deletedsuccessfully from StateCollection.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=State",
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
                        "@id": "http://localhost:8080/api/vocab?resource=EntryPoint/DatastreamCollection",
                        "@type": "hydra:Link",
                        "description": "The DatastreamCollection collection",
                        "domain": "http://localhost:8080/api/vocab?resource=EntryPoint",
                        "label": "DatastreamCollection",
                        "manages": {
                            "object": "http://localhost:8080/api/vocab?resource=Datastream",
                            "property": "rdfs:type"
                        },
                        "range": "http://localhost:8080/api/vocab?resource=DatastreamCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:datastreamcollection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all the members of DatastreamCollection",
                                "expects": "null",
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "http://localhost:8080/api/vocab?resource=Datastream",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:datastreamcollection_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new member in DatastreamCollection",
                                "expects": "http://localhost:8080/api/vocab?resource=Datastream",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "A new member in DatastreamCollection created",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Datastream",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:datastreamcollection_update",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "Update member of  DatastreamCollection ",
                                "expects": "http://localhost:8080/api/vocab?resource=Datastream",
                                "expectsHeader": [],
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "If the entity was updatedfrom DatastreamCollection.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Datastream",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:datastreamcollection_delete",
                                "@type": "http://schema.org/DeleteAction",
                                "description": "Delete member of DatastreamCollection ",
                                "expects": "http://localhost:8080/api/vocab?resource=Datastream",
                                "expectsHeader": [],
                                "method": "DELETE",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "If entity was deletedsuccessfully from DatastreamCollection.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Datastream",
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
                        "@id": "http://localhost:8080/api/vocab?resource=EntryPoint/LogEntryCollection",
                        "@type": "hydra:Link",
                        "description": "The LogEntryCollection collection",
                        "domain": "http://localhost:8080/api/vocab?resource=EntryPoint",
                        "label": "LogEntryCollection",
                        "manages": {
                            "object": "http://localhost:8080/api/vocab?resource=LogEntry",
                            "property": "rdfs:type"
                        },
                        "range": "http://localhost:8080/api/vocab?resource=LogEntryCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:logentrycollection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all the members of LogEntryCollection",
                                "expects": "null",
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "http://localhost:8080/api/vocab?resource=LogEntry",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:logentrycollection_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new member in LogEntryCollection",
                                "expects": "http://localhost:8080/api/vocab?resource=LogEntry",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "A new member in LogEntryCollection created",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=LogEntry",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:logentrycollection_update",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "Update member of  LogEntryCollection ",
                                "expects": "http://localhost:8080/api/vocab?resource=LogEntry",
                                "expectsHeader": [],
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "If the entity was updatedfrom LogEntryCollection.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=LogEntry",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:logentrycollection_delete",
                                "@type": "http://schema.org/DeleteAction",
                                "description": "Delete member of LogEntryCollection ",
                                "expects": "http://localhost:8080/api/vocab?resource=LogEntry",
                                "expectsHeader": [],
                                "method": "DELETE",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "If entity was deletedsuccessfully from LogEntryCollection.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=LogEntry",
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
                        "@id": "http://localhost:8080/api/vocab?resource=EntryPoint/CommandCollection",
                        "@type": "hydra:Link",
                        "description": "The CommandCollection collection",
                        "domain": "http://localhost:8080/api/vocab?resource=EntryPoint",
                        "label": "CommandCollection",
                        "manages": {
                            "object": "http://localhost:8080/api/vocab?resource=Command",
                            "property": "rdfs:type"
                        },
                        "range": "http://localhost:8080/api/vocab?resource=CommandCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:commandcollection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all the members of CommandCollection",
                                "expects": "null",
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "http://localhost:8080/api/vocab?resource=Command",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:commandcollection_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new member in CommandCollection",
                                "expects": "http://localhost:8080/api/vocab?resource=Command",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "A new member in CommandCollection created",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Command",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:commandcollection_update",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "Update member of  CommandCollection ",
                                "expects": "http://localhost:8080/api/vocab?resource=Command",
                                "expectsHeader": [],
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "If the entity was updatedfrom CommandCollection.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Command",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:commandcollection_delete",
                                "@type": "http://schema.org/DeleteAction",
                                "description": "Delete member of CommandCollection ",
                                "expects": "http://localhost:8080/api/vocab?resource=Command",
                                "expectsHeader": [],
                                "method": "DELETE",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "If entity was deletedsuccessfully from CommandCollection.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Command",
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
                        "@id": "http://localhost:8080/api/vocab?resource=EntryPoint/MessageCollection",
                        "@type": "hydra:Link",
                        "description": "The MessageCollection collection",
                        "domain": "http://localhost:8080/api/vocab?resource=EntryPoint",
                        "label": "MessageCollection",
                        "manages": {
                            "object": "http://localhost:8080/api/vocab?resource=Message",
                            "property": "rdfs:type"
                        },
                        "range": "http://localhost:8080/api/vocab?resource=MessageCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:messagecollection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all the members of MessageCollection",
                                "expects": "null",
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "http://localhost:8080/api/vocab?resource=Message",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:messagecollection_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new member in MessageCollection",
                                "expects": "http://localhost:8080/api/vocab?resource=Message",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "A new member in MessageCollection created",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Message",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:messagecollection_update",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "Update member of  MessageCollection ",
                                "expects": "http://localhost:8080/api/vocab?resource=Message",
                                "expectsHeader": [],
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "If the entity was updatedfrom MessageCollection.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Message",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:messagecollection_delete",
                                "@type": "http://schema.org/DeleteAction",
                                "description": "Delete member of MessageCollection ",
                                "expects": "http://localhost:8080/api/vocab?resource=Message",
                                "expectsHeader": [],
                                "method": "DELETE",
                                "possibleStatus": [
                                    {
                                        "@context": "https://www.w3.org/ns/hydra/core",
                                        "@type": "Status",
                                        "description": "If entity was deletedsuccessfully from MessageCollection.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/api/vocab?resource=Message",
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