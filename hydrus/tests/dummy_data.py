"""Creates a dummy object for a given class based on the API Documentation."""

import random
import string
import pdb


def gen_dummy_object(class_, doc):
    """Create a dummy object based on the definitions in the API Doc."""
    object_ = {
        "@type": class_
    }
    if class_ in doc.parsed_classes:
        for prop in doc.parsed_classes[class_]["class"].supportedProperty:
            if "vocab:" in prop.prop:
                prop_class = doc.parsed_classes[prop.prop.replace("vocab:", "")]["class"]
                object_[prop.title] = gen_dummy_object(prop_class, doc)
            else:
                object_[prop.title] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        return object_
