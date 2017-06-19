"""Genrate EntryPoint Context using server url, item_type."""
import json

def gen_entrypoint_context(server_url, item_type):
    SERVER_URL = server_url
    ITEM_TYPE = item_type

    entrypoint_context_template = {
        "@context": {
            "hydra": "http://www.w3.org/ns/hydra/core#",
            "vocab": SERVER_URL + "/api/vocab#",
            "EntryPoint": "vocab:EntryPoint",
            ITEM_TYPE.lower(): {
                "@id": "vocab:EntryPoint/"+ITEM_TYPE,
                "@type": "@id"
            }
        }
    }

    return json.dumps(entrypoint_context_template, indent=4)

print(gen_entrypoint_context("http://hydrus.com/", "Cots"))
