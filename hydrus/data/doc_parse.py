"""Parser for Hydra APIDocumentation creates Classes and Properties."""
from sqlalchemy import exists

from hydrus.data.db_models import RDFClass, BaseProperty
from typing import Any, Dict, List, Set, Optional
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import scoped_session
# from hydrus.tests.example_doc import doc_gen


def get_classes(apidoc: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Get all the classes in the APIDocumentation."""
    classes = list()
    for class_ in apidoc["supportedClass"]:
        if class_["@id"] not in ["http://www.w3.org/ns/hydra/core#Collection",
                                 "http://www.w3.org/ns/hydra/core#Resource", "vocab:EntryPoint"]:
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


def insert_classes(classes: List[Dict[str, Any]],
                   session: scoped_session) -> Optional[Any]:
    """Insert all the classes as defined in the APIDocumentation into DB.

    Raises:
        TypeError: If `session` is not an instance of `scoped_session` or `Session`.

    """
    # print(session.query(exists().where(RDFClass.name == "Datastream")).scalar())
    if not isinstance(session, scoped_session) and not isinstance(
            session, Session):
        raise TypeError(
            "session is not of type <sqlalchemy.orm.scoping.scoped_session>"
            "or <sqlalchemy.orm.session.Session>"
        )
    class_list = [RDFClass(name=class_["label"].strip('.')) for class_ in classes
                  if "label" in class_ and
                  not session.query(exists().where(RDFClass.name == class_["label"]
                                                   .strip('.'))).scalar()]

    class_list.extend([RDFClass(name=class_["title"].strip('.')) for class_ in classes
                       if "title" in class_ and
                       not session.query(exists().where(RDFClass.name == class_["title"]
                                                                .strip('.'))).scalar()])
    # print(class_list)
    session.add_all(class_list)
    session.commit()
    return None


def insert_properties(properties: Set[str],
                      session: scoped_session) -> Optional[Any]:
    """Insert all the properties as defined in the APIDocumentation into DB."""
    prop_list = [BaseProperty(name=prop) for prop in properties
                 if not session.query(exists().where(BaseProperty.name == prop)).scalar()]
    session.add_all(prop_list)
    session.commit()
    return None


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
