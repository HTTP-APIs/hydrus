"""Genrate EntryPoint using server url, item_type."""

import pprint

def gen_supported_operation(item_type):
    """Generate a supported operation from the op_template given the item_type."""
    ITEM_TYPE = item_type
    op_template = {
        ITEM_TYPE.lower(): "/api/%s" % (ITEM_TYPE)
    }
    return op_template

def gen_supported_ops(parsed_classes):
    """Generate a list of supported operation for entrypoint from parsed classes."""
    supported_ops = []
    for class_ in parsed_classes:
        supported_ops.append(gen_supported_operation(class_["title"]))

    return supported_ops


def gen_entrypoint(server_url, parsed_classes):
    """Generate EntryPoint."""
    SERVER_URL = server_url

    entrypoint_template = {
      "@context": "/api/contexts/EntryPoint.jsonld",
      "@id": "/api",
      "@type": "EntryPoint",
    }

    supported_ops = gen_supported_ops(parsed_classes)
    for op in supported_ops:
        entrypoint_template[list(op.keys())[0]] = op[list(op.keys())[0]]
    return entrypoint_template


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(gen_entrypoint("http://192.168.99.100:8080/"))
