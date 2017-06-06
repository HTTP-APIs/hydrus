vocab = {
    "@context": {
        "vocab": "http://hydrus.com/vocab#",
        "hydra": "http://www.w3.org/ns/hydra/core#",
        "ApiDocumentation": "hydra:ApiDocumentation",
        "property": {
            "@id": "hydra:property",
            "@type": "@id"
        },
        "readonly": "hydra:readonly",
        "writeonly": "hydra:writeonly",
        "supportedClass": "hydra:supportedClass",
        "supportedProperty": "hydra:supportedProperty",
        "supportedOperation": "hydra:supportedOperation",
        "method": "hydra:method",
        "expects": {
            "@id": "hydra:expects",
            "@type": "@id"
        },
        "returns": {
            "@id": "hydra:returns",
            "@type": "@id"
        },
        "statusCodes": "hydra:statusCodes",
        "code": "hydra:statusCode",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
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
    "@id": "http://www.markus-lanthaler.com/hydra/event-api/vocab",
    "@type": "ApiDocumentation",
    "supportedClass": [
        {
            "@id": "http://www.w3.org/ns/hydra/core#Collection",
            "@type": "hydra:Class",
            "hydra:title": "Collection",
            "hydra:description": null,
            "supportedOperation": [
            ],
            "supportedProperty": [
                {
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "hydra:title": "members",
                    "hydra:description": "The members of this collection.",
                    "required": null,
                    "readonly": false,
                    "writeonly": false
                }
            ]
        },
        {
            "@id": "http://www.w3.org/ns/hydra/core#Resource",
            "@type": "hydra:Class",
            "hydra:title": "Resource",
            "hydra:description": null,
            "supportedOperation": [
            ],
            "supportedProperty": [
            ]
        },
        {
            "@id": "http://schema.org/Event",
            "@type": "hydra:Class",
            "hydra:title": "Event",
            "hydra:description": null,
            "supportedOperation": [
                {
                    "@id": "_:event_replace",
                    "@type": "http://schema.org/UpdateAction",
                    "method": "PUT",
                    "label": "Replaces an existing Event entity",
                    "description": null,
                    "expects": "http://schema.org/Event",
                    "returns": "http://schema.org/Event",
                    "statusCodes": [
                        {
                            "code": 404,
                            "description": "If the Event entity wasn't found."
                        }
                    ]
                },
                {
                    "@id": "_:event_delete",
                    "@type": "http://schema.org/DeleteAction",
                    "method": "DELETE",
                    "label": "Deletes a Event entity",
                    "description": null,
                    "expects": null,
                    "returns": "http://www.w3.org/2002/07/owl#Nothing",
                    "statusCodes": [
                    ]
                },
                {
                    "@id": "_:event_retrieve",
                    "@type": "hydra:Operation",
                    "method": "GET",
                    "label": "Retrieves a Event entity",
                    "description": null,
                    "expects": null,
                    "returns": "http://schema.org/Event",
                    "statusCodes": [
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "property": "http://schema.org/name",
                    "hydra:title": "name",
                    "hydra:description": "The event's name",
                    "required": true,
                    "readonly": false,
                    "writeonly": false
                },
                {
                    "property": "http://schema.org/description",
                    "hydra:title": "description",
                    "hydra:description": "Description of the event",
                    "required": true,
                    "readonly": false,
                    "writeonly": false
                },
                {
                    "property": "http://schema.org/startDate",
                    "hydra:title": "start_date",
                    "hydra:description": "The start date and time of the event in ISO 8601 date format",
                    "required": true,
                    "readonly": false,
                    "writeonly": false
                },
                {
                    "property": "http://schema.org/endDate",
                    "hydra:title": "end_date",
                    "hydra:description": "The end date and time of the event in ISO 8601 date format",
                    "required": true,
                    "readonly": false,
                    "writeonly": false
                }
            ]
        },
        {
            "@id": "vocab:EntryPoint",
            "@type": "hydra:Class",
            "subClassOf": null,
            "label": "EntryPoint",
            "description": "The main entry point or homepage of the API.",
            "supportedOperation": [
                {
                    "@id": "_:entry_point",
                    "@type": "hydra:Operation",
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
                        "@id": "vocab:EntryPoint/events",
                        "@type": "hydra:Link",
                        "label": "events",
                        "description": "The events collection",
                        "domain": "vocab:EntryPoint",
                        "range": "vocab:EventCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:event_collection_retrieve",
                                "@type": "hydra:Operation",
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
                    "hydra:title": "events",
                    "hydra:description": "The events collection",
                    "required": null,
                    "readonly": true,
                    "writeonly": false
                }
            ]
        },
        {
            "@id": "vocab:EventCollection",
            "@type": "hydra:Class",
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "label": "EventCollection",
            "description": "A collection of events",
            "supportedOperation": [
                {
                    "@id": "_:event_create",
                    "@type": "http://schema.org/AddAction",
                    "method": "POST",
                    "label": "Creates a new Event entity",
                    "description": null,
                    "expects": "http://schema.org/Event",
                    "returns": "http://schema.org/Event",
                    "statusCodes": [
                        {
                          "code": 201,
                          "description": "If the Event entity was created successfully."
                        }
                    ]
                },
                {
                    "@id": "_:event_collection_retrieve",
                    "@type": "hydra:Operation",
                    "method": "GET",
                    "label": "Retrieves all Event entities",
                    "description": null,
                    "expects": null,
                    "returns": "vocab:EventCollection",
                    "statusCodes": [
                    ]
                }
            ],
            "supportedProperty": [
                {
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "hydra:title": "members",
                    "hydra:description": "The events",
                    "required": null,
                    "readonly": false,
                    "writeonly": false
                }
            ]
        }
    ]
}
