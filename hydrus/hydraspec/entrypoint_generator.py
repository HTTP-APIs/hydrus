"""Genrate EntryPoint using server url, item_type."""
import json
from hydrus.metadata.subsystem_parsed_classes import parsed_classes


def gen_supported_operation(item_type):
    """Generate a supported operation from the op_template given the item_type."""
    ITEM_TYPE = item_type
    op_template = {
        ITEM_TYPE.lower(): "/api/%s/" % (ITEM_TYPE)
    }
    return op_template

def gen_supported_ops(parsed_classes):
    """Generate a list of supported operation for entrypoint from parsed classes."""
    supported_ops = []
    for class_ in parsed_classes:
        supported_ops.append(gen_supported_operation(class_["title"]))

    return supported_ops


def gen_entrypoint(server_url):
    """Generate EntryPoint."""
    SERVER_URL = server_url

    entrypoint_template = {
      "@context": SERVER_URL + "api/contexts/EntryPoint.jsonld",
      "@id": SERVER_URL + "api/",
      "@type": "EntryPoint",
    }

    supported_ops = gen_supported_ops(parsed_classes)
    for op in supported_ops:
        entrypoint_template[op.keys()[0]] = op[op.keys()[0]]

    return json.dumps(entrypoint_template, indent=4)


if __name__ == "__main__":
    print(gen_entrypoint("http://hydrus.com/"))
