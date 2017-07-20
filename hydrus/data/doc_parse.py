"""Parser for Hydra APIDocumentation creates Classes and Properties."""
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists

from hydrus.data.db_models import RDFClass, BaseProperty, engine
# from hydrus.metadata.drone.server_doc import server_doc
# from hydrus.metadata.drone.drone_doc import drone_doc
from hydrus.metadata.doc import doc


def get_classes(apidoc):
    """Get all the classes in the APIDocumentation."""
    classes = list()
    for class_ in apidoc["supportedClass"]:
        if class_["@id"] not in ["http://www.w3.org/ns/hydra/core#Collection", "http://www.w3.org/ns/hydra/core#Resource", "vocab:EntryPoint"]:
            classes.append(class_)
    # print(classes)
    return classes


def get_all_properties(classes):
    """Get all the classes in the APIDocumentation."""
    # properties = list()
    prop_names = set()
    for class_ in classes:
        for prop in class_["supportedProperty"]:
            if prop["title"] not in prop_names:
                prop_names.add(prop["title"])
                # properties.append(prop)
    return set(prop_names)


def insert_classes(classes, session):
    """Insert all the classes as defined in the APIDocumentation into DB."""
    print(session.query(exists().where(RDFClass.name == "Datastream")).scalar())
    class_list = [RDFClass(name=class_["label"].strip('.')) for class_ in classes
                  if "label" in class_ and
                  not session.query(exists().where(RDFClass.name == class_["label"].strip('.'))).scalar()]

    class_list = class_list + [RDFClass(name=class_["title"].strip('.')) for class_ in classes
                               if "title" in class_ and
                               not session.query(exists().where(RDFClass.name == class_["title"].strip('.'))).scalar()]
    print(class_list)
    session.add_all(class_list)
    session.commit()
    return None


def insert_properties(properties, session):
    """Insert all the properties as defined in the APIDocumentation into DB."""
    prop_list = [BaseProperty(name=prop) for prop in properties
                 if not session.query(exists().where(BaseProperty.name == prop)).scalar()]
    session.add_all(prop_list)
    session.commit()
    return None


if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    session = Session()

    # Extract all classes with supportedProperty from both
    classes = get_classes(doc)

    # Extract all properties from both
    # import pdb; pdb.set_trace()
    properties = get_all_properties(classes)
    # Add all the classes
    insert_classes(classes, session)
    print("Classes inserted successfully")
    # Add all the properties
    insert_properties(properties, session)
    print("Properties inserted successfully")
