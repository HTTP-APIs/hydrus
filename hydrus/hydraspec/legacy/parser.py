"""Script to parse OWL annotations and generate a list of supported Hydra classes."""
import json
import sys

from hydrus.hydraspec.crud_template import template
from hydrus.metadata.subsystem.subsystem_vocab_jsonld import subsystem_data
import pprint


def fix_keyword(keyword):
    """Fix keyword occurances in OWL vocab. """
    if keyword == "null":
        return None
    elif keyword == "false":
        return False
    elif keyword == "true":
        return True
    else:
        return keyword


def get_all_classes(owl_data):
    """Get classes from given owl JSON-LD data."""
    classes = list()
    for obj in owl_data["defines"]:
        if obj["@type"] == "http://www.w3.org/2002/07/owl#Class":
            classes.append(obj)
    return classes


def hydrafy_class(class_, supported_props, semantic_ref_name=None):
    """Create Hydra specific Class from owl:owlClass JSON-LD."""
    hydra_class = {
        "@id": "http://api.example.com/doc/#Comment",
        "@type": "hydra:Class",
        "title": "The name of the class",
        "description": "A short description of the class.",
        "supportedProperty": [],
        "supportedOperation": []
    }
    # If there is a semantic reference name give in
    # the vocabulary then use that else use full links.

    hydra_class["@id"] = fix_keyword(class_["@id"])

    hydra_class["title"] = fix_keyword(class_["rdf:label"])
    hydra_class["description"] = fix_keyword(class_["rdf:comment"])

    supported_ops = template()
    for operation in supported_ops:
        try:
            operation["@id"] = operation["@id"] % (hydra_class["title"])
            operation["label"] = operation["label"] % (hydra_class["title"])
        except BaseException:
            print("Unexpected error:", sys.exc_info()[0])

        if operation["method"] in ["POST", "PUT"]:
            operation["expects"] = operation["expects"] % (
                hydra_class["@id"])

        if operation["method"] in ["POST", "PUT", "GET"]:
            operation["returns"] = operation["returns"] % (
                hydra_class["@id"])
        if operation["method"] in ["PUT", "GET"]:
            operation["statusCodes"][0]["description"] = operation[
                "statusCodes"][0]["description"] % (hydra_class["title"])

    additional_props = terminal_props(
        class_, supported_props, semantic_ref_name)
    hydra_class["supportedProperty"] = supported_props + additional_props
    hydra_class["supportedOperation"] = supported_ops

    return hydra_class


def hydrafy_classes(classes, properties, semantic_ref_name=None):
    """Return list of Hydrafied classes along with supported properties."""
    hydra_classes = list()
    for class_ in classes:
        supported_props = list()
        parent_class = set()
        if "rdfs:subClassOf" in class_:
            parent_class = set([fix_keyword(x["@id"])
                                for x in class_["rdfs:subClassOf"] if "@id" in x])
        # NOTE: Properties of the parent classes are inherited by child classes

        for prop in properties:
            class_list = [fix_keyword(x[0]) for x in prop["classes"]]
            if "NONE" in class_list:
                supported_props.append(prop["property"])
            elif class_["@id"] in class_list:    # Check if the class supports the property
                supported_props.append(prop["property"])
            # Check if any of the parent classes supports the property
            elif len(parent_class.intersection(set(class_list))) > 0:
                supported_props.append(prop["property"])
        hydra_classes.append(hydrafy_class(
            class_, supported_props, semantic_ref_name))
    return hydra_classes


def get_all_properties(owl_data):
    """Get properties from given owl JSON-LD data."""
    properties = list()
    for obj in owl_data["defines"]:
        obj_type = obj["@type"]
        if isinstance(obj_type, list):
            for prop in obj_type:
                if prop["@id"] == "http://www.w3.org/2002/07/owl#ObjectProperty":
                    properties.append(obj)
        elif isinstance(obj_type, dict):
            if obj_type["@id"] == "http://www.w3.org/2002/07/owl#ObjectProperty":
                properties.append(obj)

    return properties


def hydrafy_property(prop, semantic_ref_name=None):
    """Create Hydra specific Property from owl:ObjectProperty JSON-LD."""
    hydra_prop = {
        "@type": "SupportedProperty",
        "property": "#property",
        "required": False,
        "readonly": False,
        "writeonly": False
    }
    # If there is a semantic reference name give in the
    # vocabulary then use that else use full links.
    if semantic_ref_name is not None:
        hydra_prop["property"] = "{}:{}".format(
            semantic_ref_name, prop["@id"].rsplit('/', 1)[-1])
    else:
        hydra_prop["property"] = fix_keyword(prop["@id"])

    if "rdf:label" in prop:
        hydra_prop["title"] = fix_keyword(prop["rdf:label"])
    if "rdf:comment" in prop:
        hydra_prop["description"] = fix_keyword(prop["rdf:comment"])
    if "skos:prefLabel" in prop:
        hydra_prop["description"] = fix_keyword(prop["skos:prefLabel"])

    return hydra_prop


def hydrafy_properties(properties, semantic_ref_name=None):
    """Return list of Hydrafied properties along with the classes they are supported in."""
    hydra_props = list()
    for prop in properties:
        domains = [None]
        ranges = [None]
        # NOTE: No domain or range implies the property is applicable to every
        # class.
        if "rdf:domain" in prop:
            domains = [fix_keyword(x["@id"]) for x in prop["rdf:domain"]]
        if "rdf:range" in prop:
            ranges = [fix_keyword(x["@id"]) for x in prop["rdf:range"]]
        ops = [[fix_keyword(d), fix_keyword(r)]
               for d in domains for r in ranges]
        hydra_props.append({
            "property": hydrafy_property(prop, semantic_ref_name),
            "classes": ops,
        })
    return hydra_props


def terminal_props(class_, properties, semantic_ref_name=None):
    """Create terminal properties for non-descriptive property restrictions."""
    additional_props = list()
    supported_props = [fix_keyword(x["property"]) for x in properties]
    if "rdfs:subClassOf" in class_:
        for restriction in class_["rdfs:subClassOf"]:
            if "owl:onProperty" in restriction:
                if restriction["owl:onProperty"]["@id"] not in supported_props:
                    additional_props.append(hydrafy_property(
                        restriction["owl:onProperty"], semantic_ref_name))
    return additional_props


def gen_supported_classes(hydra_classes):
    """Return a list of supported classes parsed from the OWL vocabulary."""
    supported_classes = hydra_classes

    return supported_classes


if __name__ == "__main__":
    # NOTE: Usage must be in the following order
        # get_all_properties() >> hydrafy_properties() >> properties
        # get_all_classes() + properties >> hydrafy_classes() >> classes
        # classes >> gen_APIDoc()
    SEMANTIC_REF_NAME = "subsystems"

    data = subsystem_data
    # Get all the owl:ObjectProperty objects from the vocab
    owl_props = get_all_properties(data)

    # Convert each owl:ObjectProperty into a Hydra:SupportedProperty,
    # also get classes that support it based on domain and range.
    hydra_props = hydrafy_properties(owl_props, SEMANTIC_REF_NAME)

    # Get all the owl:Class objects from the vocab
    owl_classes = get_all_classes(subsystem_data)

    # Convert each owl:Class into a Hydra:Class, also get supportedProperty
    # for each
    hydra_classes = hydrafy_classes(
        owl_classes, hydra_props, SEMANTIC_REF_NAME)

    # Create API Documentation with the Hydra:Class list
    supported_classes = gen_supported_classes(hydra_classes)
    # print(fix_keyword("null"))
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(supported_classes)
