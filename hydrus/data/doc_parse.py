"""Parser for Hydra APIDocumentation creates Classes and Properties."""

import pdb
from metadata.spacecraft_apidoc import spacecraft_apidoc
from db_models import RDFClass, engine
from sqlalchemy.orm import sessionmaker
# from metadata.subsystem_apidoc import subsystem_apidoc


def get_classes(apidoc):
    """Get all the classes in the APIDocumentation."""
    classes = list()
    for class_ in apidoc["supportedClass"]:
        classes.append(class_)
    return classes


def get_all_properties(classes):
    """Get all the classes in the APIDocumentation."""
    properties = list()
    prop_names = set()
    for class_ in classes:
        for prop in class_["supportedProperty"]:
            if prop["property"] not in prop_names:
                prop_names.add(prop["property"])
                properties.append(prop)
            else:
                continue
    return properties


def insert_classes(classes):
    """Insert all the classes as defined in the APIDocumentation into DB."""
    class_list = [RDFClass(name=class_["@id"]) for class_ in classes]
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add_all(class_list)
    session.commit()
    session.close()


def insert_properties(classes):
    """Insert all the properties as defined in the APIDocumentation into DB."""
    # NOTE: Figure out a way to discriminate between abstract and instance property from APIDocumentation itself
    pass


# data = subsystem_apidoc
data = spacecraft_apidoc

classes = get_classes(data)
properties = get_all_properties(classes)
insert_classes(classes)
