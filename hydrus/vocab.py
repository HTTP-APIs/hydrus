"""Vocab and object preprocessors for Hydrus."""


def validObject(object_):
    """Check if the data passed in POST is of valid format or not."""
    if "name" in object_:
        if "@type" in object_:
            # if "object" in object_:
            return True
    return False


def struct_object(object_, type_):
    """Restructure objects submitted by Hydra Console."""
    if validObject(object_):
        return object_
    else:
        obj_temp = {
            "name": None,
            "@type": "",
            "object": {
            }}

        obj_temp["@type"] = object_.pop("@type")

        try:
            obj_temp["name"] = object_.pop("name")
        except:
            pass

        try:
            obj_temp["@context"] = object_.pop("@context")
        except:
            pass
        for prop in object_.keys():
            obj_temp["object"][prop] = object_[prop]
        return obj_temp


def get_supported_properties(parsed_classes, category, vocab):
    """Filter supported properties with their title (title, property) for a specific class from the parsed classes."""
    obj = None
    for object_ in parsed_classes:
        if object_["title"] == category:
            obj = object_
    # print(obj, category)

    supported_props = []
    if obj is not None:
        # Get object class and title
        supported_props.append((obj["title"], obj["@id"]))
        # Get supported properties
        for obj_ in obj["supportedProperty"]:
            try:
                prop = (obj_["title"], obj_["property"])

            except KeyError:
                prop = (obj_["property"].split(
                    "subsystems:")[-1], obj_["property"])

            if prop not in supported_props:
                supported_props.append(prop)
    return supported_props


def gen_context(parsed_classes, server_url, category, vocab):
    """Generate dynamic contexts for every item."""
    SERVER_URL = server_url
    PARSED_CLASSES = parsed_classes
    VOCAB = vocab
    context_template = {
        "@context": {
            "name": "http://schema.org/name",
            "object": "http://schema.org/object",
            "hydra": "http://www.w3.org/ns/hydra/core#",
            "vocab": SERVER_URL + "api/vocab#",
        }
    }

    # Get supported properties
    supported_props = get_supported_properties(PARSED_CLASSES, category, VOCAB)
    for title, value in supported_props:
        context_template["@context"][title] = value

    return context_template


def gen_collection_context(server_url, type_):
    """Generate context for Collection objects."""
    SERVER_URL = server_url
    COLLECTION_TYPE = type_.split("Collection")[0]

    template = {
        "@context": {
            "hydra": "http://www.w3.org/ns/hydra/core#",
            "vocab": SERVER_URL + "api/vocab#",
            COLLECTION_TYPE + "Collection": "vocab:%sCollection" % (COLLECTION_TYPE,),
            COLLECTION_TYPE: "vocab:%s" % (COLLECTION_TYPE,),
            "members": "http://www.w3.org/ns/hydra/core#member"
        }
    }

    return template


def hydrafy(parsed_classes, object_, collection=False):
    """Add hydra context to objects."""
    if collection:
        object_["@context"] = "/api/contexts/" + object_["@type"] + ".jsonld"
    else:
        object_["@context"] = "/api/contexts/" + object_["@type"] + ".jsonld"
    return object_
