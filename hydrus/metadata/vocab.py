#UNFINISHED
from hydrus.hydraspec.subsystem_apidoc import subsystem_apidoc
vocab = {
    "@context": {
        "vocab": "http://hydrus.com/vocab#",
        "hydraspec": "http://www.w3.org/ns/hydraspec/core#",
        "ApiDocumentation": "hydraspec:ApiDocumentation",
        "property": {
            "@id": "hydraspec:property",
            "@type": "@id"
        },
        "readonly": "hydraspec:readonly",
        "writeonly": "hydraspec:writeonly",
        "supportedClass": "hydraspec:supportedClass",
        "supportedProperty": "hydraspec:supportedProperty",
        "supportedOperation": "hydraspec:supportedOperation",
        "method": "hydraspec:method",
        "expects": {
            "@id": "hydraspec:expects",
            "@type": "@id"
        },
        "returns": {
            "@id": "hydraspec:returns",
            "@type": "@id"
        },
        "statusCodes": "hydraspec:statusCodes",
        "code": "hydraspec:statusCode",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "label": "rdfs:label",
        "description": "rdfs:comment",
        "domain": {
            "@id": "rdfs:domain",
            "@type": "@id"
        },
        "range": {
            "@id": "rdfs:range",
            "@type": "@id"
        },
        "subClassOf": {
            "@id": "rdfs:subClassOf",
            "@type": "@id"
        }
    },
    "@id": "http://hydrus.com/vocab#",
    "@type": "ApiDocumentation",
    "supportedClass": [
        {
            "@id": "http://www.w3.org/ns/hydraspec/core#Collection",
            "@type": "hydraspec:Class",
            "hydraspec:title": "Collection",
            "hydraspec:description": null,
            "supportedOperation": [
            ],
            "supportedProperty": [
                {
                    "property": "http://www.w3.org/ns/hydraspec/core#member",
                    "hydraspec:title": "members",
                    "hydraspec:description": "The members of this collection.",
                    "required": null,
                    "readonly": false,
                    "writeonly": false
                }
            ]
        },
        {
            "@id": "http://www.w3.org/ns/hydraspec/core#Resource",
            "@type": "hydraspec:Class",
            "hydraspec:title": "Resource",
            "hydraspec:description": null,
            "supportedOperation": [
            ],
            "supportedProperty": [
            ]
        },
        {
            "@id": "http://ontology.projectchronos.eu/spacecraft?format=jsonld",
            "@type": "hydraspec:Class",
            "hydraspec:title": "Spacecraft",
            "hydraspec:description": null,
            "supportedOperation": [
                {
                    "@id": "_:spacecraft_replace",
                    "@type": "http://schema.org/UpdateAction",
                    "method": "PUT",
                    "label": "Replaces an existing Spacecraft entity",
                    "description": null,
                    "expects": "http://ontology.projectchronos.eu/spacecraft?format=jsonld",
                    "returns": "http://ontology.projectchronos.eu/spacecraft?format=jsonld",
                    "statusCodes": [
                        {
                            "code": 404,
                            "description": "If the Spacecraft entity wasn't found."
                        }
                    ]
                },
                {
                    "@id": "_:spacecraft_add",
                    "@type": "http://schema.org/AddAction",
                    "method": "POST",
                    "label": "Adds a new Spacecraft entity",
                    "description": null,
                    "expects": "http://ontology.projectchronos.eu/spacecraft?format=jsonld",
                    "returns": "http://ontology.projectchronos.eu/spacecraft?format=jsonld",
                    "statusCodes": [
                    ]
                },
                {
                    "@id": "_:spacecraft_delete",
                    "@type": "http://schema.org/DeleteAction",
                    "method": "DELETE",
                    "label": "Deletes a Spacecraft entity",
                    "description": null,
                    "expects": null,
                    "returns": "http://www.w3.org/2002/07/owl#Nothing",
                    "statusCodes": [
                    ]
                },
                {
                    "@id": "_:spacecraft_retrieve",
                    "@type": "hydraspec:Operation",
                    "method": "GET",
                    "label": "Retrieves a Spacecraft entity",
                    "description": null,
                    "expects": null,
                    "returns": "http://ontology.projectchronos.eu/spacecraft?format=jsonld",
                    "statusCodes": [
                    ]
                }
            ],
            "supportedProperty": [
            # Still need to figure this part out


                # {
                #     "property": "http://schema.org/name",
                #     "hydraspec:title": "name",
                #     "hydraspec:description": "The event's name",
                #     "required": true,
                #     "readonly": false,
                #     "writeonly": false
                # },
                # {
                #     "property": "http://schema.org/description",
                #     "hydraspec:title": "description",
                #     "hydraspec:description": "Description of the event",
                #     "required": true,
                #     "readonly": false,
                #     "writeonly": false
                # },
                # {
                #     "property": "http://schema.org/startDate",
                #     "hydraspec:title": "start_date",
                #     "hydraspec:description": "The start date and time of the event in ISO 8601 date format",
                #     "required": true,
                #     "readonly": false,
                #     "writeonly": false
                # },
                # {
                #     "property": "http://schema.org/endDate",
                #     "hydraspec:title": "end_date",
                #     "hydraspec:description": "The end date and time of the event in ISO 8601 date format",
                #     "required": true,
                #     "readonly": false,
                #     "writeonly": false
                # }
            ]
        },
        {
            "@id": "http://ontology.projectchronos.eu/subsystems?format=jsonld",
            "@type": "hydraspec:Class",
            "hydraspec:title": "Cots",
            "hydraspec:description": null,
            "supportedOperation": [
                {
                    "@id": "_:cots_replace",
                    "@type": "http://schema.org/UpdateAction",
                    "method": "PUT",
                    "label": "Replaces an existing COTS entity",
                    "description": null,
                    "expects": "http://ontology.projectchronos.eu/subsystems?format=jsonld",
                    "returns": "http://ontology.projectchronos.eu/subsystems?format=jsonld",
                    "statusCodes": [
                        {
                            "code": 404,
                            "description": "If the COTS entity wasn't found."
                        }
                    ]
                },
                {
                    "@id": "_:cots_add",
                    "@type": "http://schema.org/AddAction",
                    "method": "POST",
                    "label": "Adds a new COTS entity",
                    "description": null,
                    "expects": "http://ontology.projectchronos.eu/subsystems?format=jsonld",
                    "returns": "http://ontology.projectchronos.eu/subsystems?format=jsonld",
                    "statusCodes": [
                    ]
                },
                {
                    "@id": "_:cots_delete",
                    "@type": "http://schema.org/DeleteAction",
                    "method": "DELETE",
                    "label": "Deletes a COTS entity",
                    "description": null,
                    "expects": null,
                    "returns": "http://www.w3.org/2002/07/owl#Nothing",
                    "statusCodes": [
                    ]
                },
                {
                    "@id": "_:cots_retrieve",
                    "@type": "hydraspec:Operation",
                    "method": "GET",
                    "label": "Retrieves a COTS entity",
                    "description": null,
                    "expects": null,
                    "returns": "http://ontology.projectchronos.eu/subsystems?format=jsonld",
                    "statusCodes": [
                    ]
                }
            ],
            "supportedProperty": [
            # Still need to figure this part out


                # {
                #     "property": "http://schema.org/name",
                #     "hydraspec:title": "name",
                #     "hydraspec:description": "The event's name",
                #     "required": true,
                #     "readonly": false,
                #     "writeonly": false
                # },
                # {
                #     "property": "http://schema.org/description",
                #     "hydraspec:title": "description",
                #     "hydraspec:description": "Description of the event",
                #     "required": true,
                #     "readonly": false,
                #     "writeonly": false
                # },
                # {
                #     "property": "http://schema.org/startDate",
                #     "hydraspec:title": "start_date",
                #     "hydraspec:description": "The start date and time of the event in ISO 8601 date format",
                #     "required": true,
                #     "readonly": false,
                #     "writeonly": false
                # },
                # {
                #     "property": "http://schema.org/endDate",
                #     "hydraspec:title": "end_date",
                #     "hydraspec:description": "The end date and time of the event in ISO 8601 date format",
                #     "required": true,
                #     "readonly": false,
                #     "writeonly": false
                # }
            ]
        },

        {
            "@id": "vocab:EntryPoint",
            "@type": "hydraspec:Class",
            "subClassOf": null,
            "label": "EntryPoint",
            "description": "The main entry point or homepage of the API.",
            "supportedOperation": [
                {
                    "@id": "_:entry_point",
                    "@type": "hydraspec:Operation",
                    "method": "GET",
                    "label": "The APIs main entry point.",
                    "description": null,
                    "expects": null,
                    "returns": "vocab:EntryPoint",
                    "statusCodes": [
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "property": {
                        "@id": "vocab:EntryPoint/spacecrafts",
                        "@type": "hydraspec:Link",
                        "label": "events",
                        "description": "The events collection",
                        "domain": "vocab:EntryPoint",
                        "range": "vocab:EventCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:event_collection_retrieve",
                                "@type": "hydraspec:Operation",
                                "method": "GET",
                                "label": "Retrieves all Event entities",
                                "description": null,
                                "expects": null,
                                "returns": "vocab:EventCollection",
                                "statusCodes": [
                                ]
                            }
                        ]
                    },
                    "hydraspec:title": "events",
                    "hydraspec:description": "The events collection",
                    "required": null,
                    "readonly": true,
                    "writeonly": false
                },
                {
                    "property": {
                        "@id": "vocab:EntryPoint/cots",
                        "@type": "hydraspec:Link",
                        "label": "events",
                        "description": "The events collection",
                        "domain": "vocab:EntryPoint",
                        "range": "vocab:EventCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:event_collection_retrieve",
                                "@type": "hydraspec:Operation",
                                "method": "GET",
                                "label": "Retrieves all Event entities",
                                "description": null,
                                "expects": null,
                                "returns": "vocab:EventCollection",
                                "statusCodes": [
                                ]
                            }
                        ]
                    },
                    "hydraspec:title": "events",
                    "hydraspec:description": "The events collection",
                    "required": null,
                    "readonly": true,
                    "writeonly": false
                }
            ]
        },

    ]
}
