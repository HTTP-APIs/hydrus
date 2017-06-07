"""Script to parse OWL annotations and generate Hydra API Documentation."""

from subsystem_jsonld import subsystem_data
from spacecraft_jsonld import spacecraft_data
from crud import template
import pdb
import json


def get_all_classes(owl_data):
    """Get classes from given owl JSON-LD data."""
    classes = list()
    for obj in owl_data["defines"]:
        if obj["@type"] == "http://www.w3.org/2002/07/owl#Class":
            classes.append(obj)
    return classes


def hydrafy_class(class_, supported_props):
    """Create Hydra specific Class from owl:owlClass JSON-LD."""
    hydra_class = {
      "@context": "http://www.w3.org/ns/hydra/context.jsonld",
      "@id": "http://api.example.com/doc/#Comment",
      "@type": "Class",
      "title": "The name of the class",
      "description": "A short description of the class.",
      "supportedProperty": [],
      "supportedOperation": []
    }

    hydra_class["@id"] = class_["@id"]
    hydra_class["title"] = class_["rdf:label"]
    hydra_class["description"] = class_["rdf:comment"]

    supported_ops = template()
    for operation in supported_ops:
        try:
            operation["@id"] = operation["@id"] % (hydra_class["title"])
            operation["label"] = operation["label"] % (hydra_class["title"])
        except:
            pdb.set_trace()
        if operation["method"] in ["POST", "PUT"]:
            operation["expects"] = operation["expects"] % (hydra_class["@id"])
        if operation["method"] in ["POST", "PUT", "GET"]:
            operation["returns"] = operation["returns"] % (hydra_class["@id"])
        if operation["method"] in ["PUT", "GET"]:
            operation["statusCodes"][0]["description"] = operation["statusCodes"][0]["description"] % (hydra_class["title"])

    additional_props = terminal_props(class_, supported_props)
    hydra_class["supportedProperty"] = supported_props + additional_props
    hydra_class["supportedOperation"] = supported_ops

    return hydra_class


def hydrafy_classes(classes, properties):
    """Return list of Hydrafied classes along with supported properties."""
    hydra_classes = list()
    for class_ in classes:
        supported_props = list()
        parent_class = set()
        if "rdfs:subClassOf" in class_:
            parent_class = set([x["@id"] for x in class_["rdfs:subClassOf"] if "@id" in x])
        # NOTE: Properties of the parent classes are inherited by child classes

        for prop in properties:
            class_list = [x[0] for x in prop["classes"]]
            if "NONE" in class_list:
                supported_props.append(prop["property"])
            elif class_["@id"] in class_list:    # Check if the class supports the property
                supported_props.append(prop["property"])
            elif len(parent_class.intersection(set(class_list))) > 0:   # Check if any of the parent classes supports the property
                supported_props.append(prop["property"])
        hydra_classes.append(hydrafy_class(class_, supported_props))
    return hydra_classes


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
      "required": "false",
      "readonly": "false",
      "writeonly": "false"
    }
    hydra_prop["property"] = prop["@id"]
    if "rdf:label" in prop:
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
        ops = [[d, r] for d in domains for r in ranges]
        hydra_props.append({
            "property": hydrafy_property(prop),
            "classes": ops,
        })
    return hydra_props


def terminal_props(class_, properties):
    """Create terminal properties for non-descriptive property restrictions."""
    additional_props = list()
    supported_props = [x["property"] for x in properties]
    if "rdfs:subClassOf" in class_:
        for restriction in class_["rdfs:subClassOf"]:
            if "owl:onProperty" in restriction:
                if restriction["owl:onProperty"]["@id"] not in supported_props:
                    additional_props.append(hydrafy_property(restriction["owl:onProperty"]))
    return additional_props


def gen_APIDoc(hydra_classes):
    """Generate Hydra API Documentation for given hydra classes."""
    template = {
      "@context": "http://www.w3.org/ns/hydra/context.jsonld",
      "@id": "http://api.example.com/doc/",
      "@type": "ApiDocumentation",
      "title": "The name of the API",
      "description": "A short description of the API",
      "entrypoint": "URL of the API's main entry point",
      "supportedClass": [
      ],
      "possibleStatus": [
      ]
    }
    template["supportedClass"] = hydra_classes
    return template


if __name__ == "__main__":
    # NOTE: Usage must be in the following order
        # get_all_properties() >> hydrafy_properties() >> properties
        # get_all_classes() + properties >> hydrafy_classes() >> classes
        # classes >> gen_APIDoc()

    data = subsystem_data
    # Get all the owl:ObjectProperty objects from the vocab
    owl_props = get_all_properties(data)

    # Convert each owl:ObjectProperty into a Hydra:SupportedProperty, also get classes that support it based on domain and range.
    hydra_props = hydrafy_properties(owl_props)

    # Get all the owl:Class objects from the vocab
    owl_classes = get_all_classes(subsystem_data)

    # Convert each owl:Class into a Hydra:Class, also get supportedProperty for each
    hydra_classes = hydrafy_classes(owl_classes, hydra_props)

    # Create API Documentation with the Hydra:Class list
    apidoc = gen_APIDoc(hydra_classes)

    print(json.dumps(apidoc, indent=4))
