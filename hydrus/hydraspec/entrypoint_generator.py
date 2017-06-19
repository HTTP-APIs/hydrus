"""Genrate EntryPoint using server url, item_type."""
import json

def gen_entrypoint(server_url, item_type):
    SERVER_URL = server_url
    ITEM_TYPE = item_type

    entrypoint_template = {
  "@context": SERVER_URL + "api/contexts/EntryPoint.jsonld",
  "@id": SERVER_URL+ "api/",
  "@type": "EntryPoint",
  ITEM_TYPE.lower(): "api/%s/"%(ITEM_TYPE.lower())
}

    return json.dumps(entrypoint_template, indent=4)

print(gen_entrypoint("http://hydrus.com/", "Cots"))
