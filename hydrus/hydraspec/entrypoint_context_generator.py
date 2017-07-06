"""Genrate EntryPoint Context using server url, item_type."""

import pprint



def gen_supported_operation(item_type):
    """Generate a supported operation from op_template given item type."""
    ITEM_TYPE = item_type
    op_template = {
        ITEM_TYPE.lower(): {
            "@id": "vocab:EntryPoint/"+ITEM_TYPE,
            "@type": "@id"
        }
    }
    return op_template\


def gen_supported_ops(parsed_classes):
    """Generate list of supported operations from parsed classes for entrypoint context."""
    supported_ops = []
    for class_ in parsed_classes:
        supported_ops.append(gen_supported_operation(class_["title"]))

    return supported_ops


def gen_entrypoint_context(server_url, parsed_classes):
    """Generate context for the EntryPoint."""
    SERVER_URL = server_url

    entrypoint_context_template = {
        "@context": {
            "hydra": "http://www.w3.org/ns/hydra/core#",
            "vocab": SERVER_URL + "api/vocab#",
            "EntryPoint": "vocab:EntryPoint",
            ##Supported Operations will be appended here
        }
    }
    supported_ops = gen_supported_ops(parsed_classes)
    for op in supported_ops:
        entrypoint_context_template["@context"][list(op.keys())[0]] = op[list(op.keys())[0]]
    return entrypoint_context_template


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(gen_entrypoint_context(SERVER_URL))
