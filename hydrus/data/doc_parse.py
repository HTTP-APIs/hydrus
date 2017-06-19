"""Parser for Hydra APIDocumentation creates Classes and Properties."""
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists

from hydrus.data.db_models import RDFClass, BaseProperty, engine
from hydrus.hydraspec.spacecraft_apidoc import spacecraft_apidoc
from hydrus.hydraspec.subsystem_apidoc import subsystem_apidoc


def get_classes(apidoc):
    """Get all the classes in the APIDocumentation."""
    classes = list()
    for class_ in apidoc["supportedClass"]:
        classes.append(class_)
    return classes


def get_all_properties(classes):
    """Get all the classes in the APIDocumentation."""
    # properties = list()
    prop_names = set()
    for class_ in classes:
        for prop in class_["supportedProperty"]:
            if prop["property"] not in prop_names:
                prop_names.add(prop["property"].split('/')[-1])
                # properties.append(prop)
    return set(prop_names)


def insert_classes(classes):
    """Insert all the classes as defined in the APIDocumentation into DB."""
    Session = sessionmaker(bind=engine)
    session = Session()
    class_list = [RDFClass(name=class_["title"]) for class_ in classes
                  if not session.query(exists().where(RDFClass.name == class_["title"])).scalar()]
    session.add_all(class_list)
    session.commit()
    session.close()
    return None


def insert_properties(properties):
    """Insert all the properties as defined in the APIDocumentation into DB."""
    Session = sessionmaker(bind=engine)
    session = Session()
    prop_list = [BaseProperty(name=prop) for prop in properties
                 if not session.query(exists().where(BaseProperty.name == prop)).scalar()]
    session.add_all(prop_list)
    session.commit()
    session.close()
    return None


if __name__ == "__main__":
    # Get the API Doc for both vocabularies
    spacecraft_data = spacecraft_apidoc
    subsystem_data = subsystem_apidoc
    # Extract all classes with supportedProperty from both
    spacecraft_classes = get_classes(spacecraft_data)
    spacecraft_properties = get_all_properties(spacecraft_classes)
    # Extract all properties from both
    subsystem_classes = get_classes(subsystem_data)
    subsystem_properties = get_all_properties(subsystem_classes)
    # Add all the classes
    insert_classes(spacecraft_classes)
    insert_classes(subsystem_classes)
    # Add all the properties
    insert_properties(spacecraft_properties)
    insert_properties(subsystem_properties)
