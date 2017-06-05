"""Script to parse OWL annotations and generate Hydra API Documentation."""

from subsystem_jsonld import subsystem_data
from spacecraft_jsonld import spacecraft_data
import pdb
import json


def get_all_classes(owl_data):
    """Get classes from given owl JSON-LD data."""
    classes = list()
    for obj in owl_data["defines"]:
        if obj["@type"] == "http://www.w3.org/2002/07/owl#Class":
            classes.append(obj)
    return classes


def hydrafy_classes(classes, properties):
    """Create Hydra specific Class from owl:owlClass JSON-LD."""
    hydra_classes = list()
    for class_ in classes:
        supported_props = list()
        parent_class = set([x["@id"] for x in class_["rdf:subClassOf"]])
        # NOTE: Properties of the parent classes are inherited by child classes

        for prop in properties:
            class_list = [x[0] for x in prop["classes"]]
            if class_["@id"] in class_list:     # Check if the class supports the property
                supported_props.append(prop)
            elif len(parent_class.intersection(set(class_list))) > 0:   # Check if any of the parent classes supports the property
                supported_props.append(prop)







def get_all_properties(owl_data):
    """Get properties from given owl JSON-LD data."""
    properties = list()
    for obj in owl_data["defines"]:
        obj_type = obj["@type"]
        if type(obj_type) == list:
            for prop in obj_type:
                if prop["@id"] == "http://www.w3.org/2002/07/owl#ObjectProperty":
                    properties.append(obj)
        elif type(obj_type) == dict:
            if obj_type["@id"] == "http://www.w3.org/2002/07/owl#ObjectProperty":
                properties.append(obj)

    return properties


def hydrafy_property(prop):
    """Create Hydra specific Property from owl:ObjectProperty JSON-LD."""
    hydra_prop = {
      "@type": "SupportedProperty",
      "property": "#property",
      "title": "random title",
      "description": "can do blah..",
      "required": "false",
      "readonly": "false",
      "writeonly": "false"
    }
    hydra_prop["property"] = prop["@id"]
    hydra_prop["title"] = prop["rdf:label"]
    if "rdf:comment" in prop:
        hydra_prop["description"] = prop["rdf:comment"]
    if "skos:prefLabel" in prop:
        hydra_prop["description"] = prop["skos:prefLabel"]

    return hydra_prop


def hydrafy_properties(properties):
    """Return list of Hydrafied properties along with the classes they are supported in."""
    hydra_props = list()
    for prop in properties:
        domains = ["NONE"]
        ranges = ["NONE"]
        # NOTE: No domain or range implies the property is applicable to every class.
        if "rdf:domain" in prop:
            domains = [x["@id"] for x in prop["rdf:domain"]]
        if "rdf:range" in prop:
            ranges = [x["@id"] for x in prop["rdf:range"]]
        ops = [(d, r) for d in domains for r in ranges]
        hydra_props.append({
            "property": hydrafy_property(prop),
            "classes": ops,
        })
    return hydra_props


# Get all the owl:ObjectProperty objects from the vocab
owl_props = get_all_properties(subsystem_data)

# Convert each owl:ObjectProperty into a Hydra:SupportedProperty, also get classes that support it based on domain and range.
hydra_props = hydrafy_properties(owl_props)

# Get all the owl:Class objects from the vocab
owl_classes = get_all_classes(subsystem_data)
print(json.dumps(owl_classes, indent=4))
pdb.set_trace()
