"""Parser for Hydra APIDocumentation creates Classes and Properties."""

from typing import Any, Dict, List, Set, Optional
from hydra_python_core.doc_writer import HydraDoc


def get_classes(apidoc: HydraDoc) -> List[Dict[str, Any]]:
    """Get all the classes in the APIDocumentation."""
    COLLECTION_ID = "http://www.w3.org/ns/hydra/core#Collection"
    RESOURCE_ID = "http://www.w3.org/ns/hydra/core#Resource"
    ENTRYPOINT_ID = apidoc.entrypoint.entrypoint.id_
    classes = []
    for class_ in apidoc.generate()["supportedClass"]:
        if class_["@id"] not in [COLLECTION_ID, RESOURCE_ID, ENTRYPOINT_ID]:
            classes.append(class_)
    # print(classes)
    return classes


def get_all_properties(classes: List[Dict[str, Any]]) -> Set[str]:
    """Get all the properties in the APIDocumentation."""
    # properties = list()
    prop_names = set()  # type: Set[str]
    for class_ in classes:
        for prop in class_["supportedProperty"]:
            if prop["title"] not in prop_names:
                prop_names.add(prop["title"])
                # properties.append(prop)
    return set(prop_names)


# if __name__ == "__main__":
#     Session = sessionmaker(bind=engine)
#     session = Session()
#
#     doc = doc_gen("test", "test")
#     # Extract all classes with supportedProperty from both
#     classes = get_classes(doc.generate())
#
#     # Extract all properties from both
#     # import pdb; pdb.set_trace()
#     properties = get_all_properties(classes)
#     # Add all the classes
#     insert_classes(classes, session)
#     print("Classes inserted successfully")
#     # Add all the properties
#     insert_properties(properties, session)
#     print("Properties inserted successfully")
