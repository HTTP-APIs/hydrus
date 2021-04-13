"""Generated API Documentation sample using doc_writer_sample.py."""

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
        "writeable": "hydra:writeable"
    },
    "@id": "http://localhost:8080/movie_api/vocab",
    "@type": "ApiDocumentation",
    "description": "This API lets you see the list of good movies and gives you the ability to modify the list",
    "entrypoint": "http://localhost:8080/movie_api",
    "possibleStatus": [],
    "supportedClass": [
        {
            "@id": "http://localhost:8080/movie_api/vocab#Movie",
            "@type": "hydra:Class",
            "description": "The class of the Movie",
            "supportedOperation": [
                {
                    "@type": "http://schema.org/UpdateAction",
                    "expects": "http://localhost:8080/movie_api/vocab#Movie",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Movie class updated.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [
                        "Content-Type",
                        "Content-Length"
                    ],
                    "title": "UpdateMovie"
                },
                {
                    "@type": "http://schema.org/AddAction",
                    "expects": "http://localhost:8080/movie_api/vocab#Movie",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Movie class Added.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [
                        "Content-Type",
                        "Content-Length"
                    ],
                    "title": "AddMovie"
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
                            "description": "Movie class returned.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/movie_api/vocab#Movie",
                    "returnsHeader": [
                        "Content-Type",
                        "Content-Length"
                    ],
                    "title": "GetMovie"
                },
                {
                    "@type": "http://schema.org/DeleteAction",
                    "expects": "http://localhost:8080/movie_api/vocab#Movie",
                    "expectsHeader": [],
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "Movie class deleted.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "null",
                    "returnsHeader": [
                        "Content-Type",
                        "Content-Length"
                    ],
                    "title": "DeleteMovie"
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/name",
                    "readable": "true",
                    "required": "true",
                    "title": "movie_name",
                    "writeable": "true"
                },
                {
                    "@type": "SupportedProperty",
                    "property": "http://schema.org/director",
                    "readable": "true",
                    "required": "true",
                    "title": "movie_director",
                    "writeable": "true"
                }
            ],
            "title": "Movie"
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
            "@id": "http://localhost:8080/movie_api/vocab#MovieCollection",
            "@type": "Collection",
            "description": "This collection comprises of all the objects of type Movie",
            "manages": {
                "object": "http://localhost:8080/movie_api/vocab#Movie",
                "property": "rdf:type"
            },
            "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
            "supportedOperation": [
                {
                    "@id": "_:MovieCollection_retrieve",
                    "@type": "http://schema.org/FindAction",
                    "description": "Retrieves all the members of MovieCollection",
                    "expects": "null",
                    "expectsHeader": [],
                    "method": "GET",
                    "possibleStatus": [],
                    "returns": "http://localhost:8080/movie_api/vocab#Movie",
                    "returnsHeader": []
                },
                {
                    "@id": "_:MovieCollection_create",
                    "@type": "http://schema.org/AddAction",
                    "description": "Create new member in MovieCollection",
                    "expects": "http://localhost:8080/movie_api/vocab#Movie",
                    "expectsHeader": [],
                    "method": "PUT",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "A new member in MovieCollection created",
                            "statusCode": 201,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/movie_api/vocab#Movie",
                    "returnsHeader": []
                },
                {
                    "@id": "_:MovieCollection_update",
                    "@type": "http://schema.org/UpdateAction",
                    "description": "Update member of  MovieCollection ",
                    "expects": "http://localhost:8080/movie_api/vocab#Movie",
                    "expectsHeader": [],
                    "method": "POST",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "If the entity was updatedfrom MovieCollection.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/movie_api/vocab#Movie",
                    "returnsHeader": []
                },
                {
                    "@id": "_:MovieCollection_delete",
                    "@type": "http://schema.org/DeleteAction",
                    "description": "Delete member of MovieCollection ",
                    "expects": "http://localhost:8080/movie_api/vocab#Movie",
                    "expectsHeader": [],
                    "method": "DELETE",
                    "possibleStatus": [
                        {
                            "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                            "@type": "Status",
                            "description": "If entity was deletedsuccessfully from MovieCollection.",
                            "statusCode": 200,
                            "title": ""
                        }
                    ],
                    "returns": "http://localhost:8080/movie_api/vocab#Movie",
                    "returnsHeader": []
                }
            ],
            "supportedProperty": [
                {
                    "@type": "SupportedProperty",
                    "description": "The members of MovieCollection",
                    "property": "http://www.w3.org/ns/hydra/core#member",
                    "readable": "false",
                    "required": "false",
                    "title": "members",
                    "writeable": "false"
                }
            ],
            "title": "MovieCollection"
        },
        {
            "@id": "http://localhost:8080/movie_api#EntryPoint",
            "@type": "hydra:Class",
            "description": "The main entry point or homepage of the API.",
            "supportedOperation": [
                {
                    "@id": "_:entry_point",
                    "@type": "http://localhost:8080//movie_api#EntryPoint",
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
                    "hydra:description": "The Movie Class",
                    "hydra:title": "movie",
                    "property": {
                        "@id": "http://localhost:8080/movie_api/vocab#EntryPoint/Movie",
                        "@type": "hydra:Link",
                        "description": "The class of the Movie",
                        "domain": "http://localhost:8080/movie_api/vocab#EntryPoint",
                        "label": "Movie",
                        "range": "http://localhost:8080/movie_api/vocab#Movie",
                        "supportedOperation": [
                            {
                                "@id": "updatemovie",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "null",
                                "expects": "http://localhost:8080/movie_api/vocab#Movie",
                                "expectsHeader": [],
                                "label": "UpdateMovie",
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "Movie class updated.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "null",
                                "returnsHeader": [
                                    "Content-Type",
                                    "Content-Length"
                                ]
                            },
                            {
                                "@id": "addmovie",
                                "@type": "http://schema.org/AddAction",
                                "description": "null",
                                "expects": "http://localhost:8080/movie_api/vocab#Movie",
                                "expectsHeader": [],
                                "label": "AddMovie",
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "Movie class Added.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "null",
                                "returnsHeader": [
                                    "Content-Type",
                                    "Content-Length"
                                ]
                            },
                            {
                                "@id": "getmovie",
                                "@type": "http://schema.org/FindAction",
                                "description": "null",
                                "expects": "null",
                                "expectsHeader": [],
                                "label": "GetMovie",
                                "method": "GET",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "Movie class returned.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/movie_api/vocab#Movie",
                                "returnsHeader": [
                                    "Content-Type",
                                    "Content-Length"
                                ]
                            },
                            {
                                "@id": "deletemovie",
                                "@type": "http://schema.org/DeleteAction",
                                "description": "null",
                                "expects": "http://localhost:8080/movie_api/vocab#Movie",
                                "expectsHeader": [],
                                "label": "DeleteMovie",
                                "method": "DELETE",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "Movie class deleted.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "null",
                                "returnsHeader": [
                                    "Content-Type",
                                    "Content-Length"
                                ]
                            }
                        ]
                    },
                    "readable": "true",
                    "required": "null",
                    "writeable": "false"
                },
                {
                    "hydra:description": "The MovieCollection collection",
                    "hydra:title": "moviecollection",
                    "property": {
                        "@id": "http://localhost:8080/movie_api/vocab#EntryPoint/MovieCollection",
                        "@type": "hydra:Link",
                        "description": "The MovieCollection collection",
                        "domain": "http://localhost:8080/movie_api/vocab#EntryPoint",
                        "label": "MovieCollection",
                        "manages": {
                            "object": "http://localhost:8080/movie_api/vocab#Movie",
                            "property": "rdf:type"
                        },
                        "range": "http://localhost:8080/movie_api/vocab#MovieCollection",
                        "supportedOperation": [
                            {
                                "@id": "_:moviecollection_retrieve",
                                "@type": "http://schema.org/FindAction",
                                "description": "Retrieves all the members of MovieCollection",
                                "expects": "null",
                                "expectsHeader": [],
                                "method": "GET",
                                "possibleStatus": [],
                                "returns": "http://localhost:8080/movie_api/vocab#Movie",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:moviecollection_create",
                                "@type": "http://schema.org/AddAction",
                                "description": "Create new member in MovieCollection",
                                "expects": "http://localhost:8080/movie_api/vocab#Movie",
                                "expectsHeader": [],
                                "method": "PUT",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "A new member in MovieCollection created",
                                        "statusCode": 201,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/movie_api/vocab#Movie",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:moviecollection_update",
                                "@type": "http://schema.org/UpdateAction",
                                "description": "Update member of  MovieCollection ",
                                "expects": "http://localhost:8080/movie_api/vocab#Movie",
                                "expectsHeader": [],
                                "method": "POST",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "If the entity was updatedfrom MovieCollection.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/movie_api/vocab#Movie",
                                "returnsHeader": []
                            },
                            {
                                "@id": "_:moviecollection_delete",
                                "@type": "http://schema.org/DeleteAction",
                                "description": "Delete member of MovieCollection ",
                                "expects": "http://localhost:8080/movie_api/vocab#Movie",
                                "expectsHeader": [],
                                "method": "DELETE",
                                "possibleStatus": [
                                    {
                                        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
                                        "@type": "Status",
                                        "description": "If entity was deletedsuccessfully from MovieCollection.",
                                        "statusCode": 200,
                                        "title": ""
                                    }
                                ],
                                "returns": "http://localhost:8080/movie_api/vocab#Movie",
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
    "title": "The Description for the movie API"
}