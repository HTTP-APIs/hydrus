"""Genrate hydra vocabulary using parsed classes, server url, item_type and item_semantic_url."""

import pprint


def gen_entrypoint_supported_prop(item_type):
    """Generate SupportedProperty for item_type from property template
     from Markus Lanthler's event api example."""
    ITEM_TYPE = item_type
    prop_template = {
        "property": {
            "@id": "vocab:EntryPoint/" + ITEM_TYPE,
            "@type": "hydra:Link",
            "label": ITEM_TYPE,
            "description": "The %s collection" % (ITEM_TYPE,),
            "domain": "vocab:EntryPoint",
            "range": "vocab:%sCollection" % (ITEM_TYPE,),
            "supportedOperation": [
                {
                    "@id": "_:%s_collection_retrieve" % (ITEM_TYPE.lower(),),
                    "@type": "hydra:Operation",
                    "method": "GET",
                    "label": "Retrieves all %s entities" % (ITEM_TYPE,),
                    "description": None,
                    "expects": None,
                    "returns": "vocab:%sCollection" % (ITEM_TYPE,),
                    "statusCodes": [
                    ]
                }
            ]
        },
        "hydra:title": ITEM_TYPE.lower(),
        "hydra:description": "The %s collection" % (ITEM_TYPE,),
        "required": None,
        "readonly": True,
        "writeonly": False
    }
    return prop_template


def gen_entrypoint_supported_props(parsed_classes):
    """Generate supported properties from parsed_classes for Entrypoint["supportedProperty"]."""
    supported_props = []
    for class_ in parsed_classes:
        supported_props.append(gen_entrypoint_supported_prop(class_["title"]))
    return supported_props


def gen_item_collection(semantic_ref_name, item_):
    """Generate ItemCollection for item_type from collection_template
     from Markus Lanthler's event api example."""
    SEMANTIC_REF_NAME = semantic_ref_name
    ITEM_  = item_
    ITEM_TYPE = ITEM_["title"]

    collection_template = {
        "@id": "vocab:%sCollection" % (ITEM_TYPE,),
        "@type": "hydra:Class",
        "subClassOf": "http://www.w3.org/ns/hydra/core#Collection",
        "label": "%sCollection" % (ITEM_TYPE),
        "description": "A collection of %s" % (ITEM_TYPE.lower()),
        "supportedOperation": [
            {
                "@id": "_:%s_create" % (ITEM_TYPE.lower()),
                "@type": "http://schema.org/AddAction",
                "method": "POST",
                "description": None,
                "expects": [x["expects"] for x in ITEM_["supportedOperation"]][0] if [x["expects"] for x in ITEM_["supportedOperation"]][0] else None ,
                "returns": [x["returns"] for x in ITEM_["supportedOperation"]][0] if [x["returns"] for x in ITEM_["supportedOperation"]][0] else None,
                "statusCodes": [
                    {
                        "code": 201,
                        "description": "If the %s entity was created successfully." % (ITEM_TYPE,)
                    }
                ]
            },
            {
                "@id": "_:%s_collection_retrieve" % (ITEM_TYPE.lower(),),
                "@type": "hydra:Operation",
                "method": "GET",
                "label": "Retrieves all %s entities" % (ITEM_TYPE,),
                "description": None,
                "expects": None,
                "returns": "vocab:%sCollection" % (ITEM_TYPE),
                "statusCodes": [
                ]
            }
        ],
        "supportedProperty": [
            {
                "property": "http://www.w3.org/ns/hydra/core#member",
                "hydra:title": "members",
                "hydra:description": "The %s" % (ITEM_TYPE.lower(),),
                "required": None,
                "readonly": False,
                "writeonly": False

            }
        ]
    }

    return collection_template


def gen_item_collection_list(semantic_ref_name, parsed_classes):
    """Generate a list of item collections for the vocab."""
    collections = []
    for class_ in parsed_classes:
        collections.append(gen_item_collection(
            semantic_ref_name, class_))
    return collections


def gen_vocab(parsed_classes, server_url, semantic_ref_name, semantic_ref_url):
    """Generate Hydra Vocabulary."""
    SERVER_URL = server_url
    SEMANTIC_REF_NAME = semantic_ref_name
    SEMANTIC_REF_URL = semantic_ref_url

    vocab_template = {
        "@context": {
            "vocab": SERVER_URL + "api/vocab#",
            "hydra": "http://www.w3.org/ns/hydra/core#",
            SEMANTIC_REF_NAME: SEMANTIC_REF_URL,
            "ApiDocumentation": "hydra:ApiDocumentation",
            "property": {
                "@id": "hydra:property",
                "@type": "@id"
            },
            "readonly": "hydra:readonly",
            "writeonly": "hydra:writeonly",
            "title":"hydra:title",
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
            "owl": "http://www.w3.org/2002/07/owl#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "label": "rdfs:label",
            "description": "rdfs:comment",
            "subClassOf": {
                "@id": "rdfs:subClassOf",
                "@type": "@id"
            },
            "domain": {
              "@id": "rdfs:domain",
              "@type": "@id"
            },
            "range": {
              "@id": "rdfs:range",
              "@type": "@id"
            },
        },
        "@id": SERVER_URL + "api/vocab",
        "@type": "ApiDocumentation",
        "supportedClass": [
            {
                "@id": "http://www.w3.org/ns/hydra/core#Collection",
                "@type": "hydra:Class",
                "hydra:title": "Collection",
                "hydra:description": None,
                "supportedOperation": [
                ],
                "supportedProperty": [
                    {
                        "property": "http://www.w3.org/ns/hydra/core#member",
                        "hydra:title": "members",
                        "hydra:description": "The members of this collection.",
                        "required": None,
                        "readonly": False,
                        "writeonly": False
                    }
                ]
            },
            {
                "@id": "http://www.w3.org/ns/hydra/core#Resource",
                "@type": "hydra:Class",
                "hydra:title": "Resource",
                "hydra:description": None,
                "supportedOperation": [
                ],
                "supportedProperty": [
                ]
            },
            {
                "@id": "vocab:EntryPoint",
                "@type": "hydra:Class",
                "subClassOf": None,
                "label": "EntryPoint",
                "description": "The main entry point or homepage of the API.",
                "supportedOperation": [
                    {
                        "@id": "_:entry_point",
                        "@type": "hydra:Operation",
                        "method": "GET",
                        "label": "The APIs main entry point.",
                        "description": None,
                        "expects": None,
                        "returns": "vocab:EntryPoint",
                        "statusCodes": [
                        ]
                    }
                ],
                "supportedProperty": gen_entrypoint_supported_props(parsed_classes)
            },
            # Parsed classed from hydrus.hydraspec.parser will be added here

        ]
    }
    #Add parsed hydra classes to the vocabulary
    for class_ in parsed_classes:
        vocab_template["supportedClass"].append(class_)

    #Add different item collections to the hydra vocabulary
    collection_list = gen_item_collection_list(semantic_ref_name, parsed_classes)
    for collection_item in collection_list:
        vocab_template["supportedClass"].append(collection_item)

    return vocab_template


if __name__ == "__main__":
    # DEMO
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(gen_vocab(parsed_classes, SERVER_URL, "subsystems",
          "http://ontology.projectchronos.eu/subsystems"))
