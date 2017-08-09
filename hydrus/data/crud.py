"""Basic CRUD operations for the server."""

from sqlalchemy.orm import with_polymorphic
from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound
from hydrus.data.db_models import (Graph, BaseProperty, RDFClass, Instance,
                                   Terminal, GraphIAC, GraphIIT, GraphIII)

from hydrus.data.exceptions import (ClassNotFound, InstanceExists, PropertyNotFound,
                                    NotInstanceProperty, NotAbstractProperty,
                                    InstanceNotFound)

triples = with_polymorphic(Graph, '*')
properties = with_polymorphic(BaseProperty, "*")


def get(id_, type_, api_name, session, recursive=False):
    """Retrieve an Instance with given ID from the database [GET]."""
    object_template = {
        "@type": "",
    }
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == type_).one()
    except NoResultFound:
        raise ClassNotFound(type_=type_)

    try:
        instance = session.query(Instance).filter(
            Instance.id == id_, Instance.type_ == rdf_class.id).one()
    except NoResultFound:
        raise InstanceNotFound(type_=rdf_class.name, id_=id_)

    data_IAC = session.query(triples).filter(triples.GraphIAC.subject == id_).all()

    data_III = session.query(triples).filter(triples.GraphIII.subject == id_).all()

    data_IIT = session.query(triples).filter(triples.GraphIIT.subject == id_).all()

    for data in data_IAC:
        prop_name = session.query(properties).filter(properties.id == data.predicate).one().name
        class_name = session.query(RDFClass).filter(RDFClass.id == data.object_).one().name
        object_template[prop_name] = class_name

    for data in data_III:
        prop_name = session.query(properties).filter(properties.id == data.predicate).one().name
        instance = session.query(Instance).filter(Instance.id == data.object_).one()
        # Get class name for instance object
        inst_class_name = session.query(RDFClass).filter(RDFClass.id == instance.type_).one().name
        # Recursive call should get the instance needed
        object_ = get(id_=instance.id, type_=inst_class_name, session=session, recursive=True, api_name=api_name)
        object_template[prop_name] = object_

    for data in data_IIT:
        prop_name = session.query(properties).filter(properties.id == data.predicate).one().name
        terminal = session.query(Terminal).filter(Terminal.id == data.object_).one()
        try:
            object_template[prop_name] = terminal.value
        except:
            # If terminal is none
            object_template[prop_name] = ""
    object_template["@type"] = rdf_class.name
    if not recursive:
        object_template["@id"] = "/"+api_name+"/"+type_+"/"+str(id_)

    return object_template


def insert(object_, session, id_=None):
    """Insert an object to database [POST] and returns the inserted object."""
    rdf_class = None
    instance = None

    # Check for class in the begging
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == object_["@type"]).one()
    except NoResultFound:
        raise ClassNotFound(type_=object_["@type"])

    if id_ is not None:
        if session.query(exists().where(Instance.id == id_)).scalar():
            raise InstanceExists(type_=rdf_class.name, id_=id_)
        else:
            instance = Instance(id=id_, type_=rdf_class.id)
    else:
        instance = Instance(type_=rdf_class.id)
    session.add(instance)
    session.flush()

    for prop_name in object_:
        if prop_name not in ["@type", "@context"]:
            try:
                property_ = session.query(properties).filter(
                    properties.name == prop_name).one()
            except NoResultFound:
                # Adds new Property
                session.close()
                raise PropertyNotFound(type_=prop_name)

            # For insertion in III
            if type(object_[prop_name]) == dict:
                instance_id = insert(object_[prop_name], session=session)
                instance_object = session.query(Instance).filter(Instance.id == instance_id).one()

                if property_.type_ == "PROPERTY" or property_.type_ == "INSTANCE":
                    property_.type_ = "INSTANCE"
                    session.add(property_)
                    triple = GraphIII(subject=instance.id, predicate=property_.id, object_=instance_object.id)
                    session.add(triple)
                else:
                    session.close()
                    raise NotInstanceProperty(type_=prop_name)

            # For insertion in IAC
            elif session.query(exists().where(RDFClass.name == str(object_[prop_name]))).scalar():
                if property_.type_ == "PROPERTY" or property_.type_ == "ABSTRACT":
                    property_.type_ = "ABSTRACT"
                    session.add(property_)
                    class_ = session.query(RDFClass).filter(RDFClass.name == object_[prop_name]).one()
                    triple = GraphIAC(subject=instance.id, predicate=property_.id, object_=class_.id)
                    session.add(triple)
                else:
                    session.close()
                    raise NotAbstractProperty(type_=prop_name)

            # For insertion in IIT
            else:
                terminal = Terminal(value=object_[prop_name])
                session.add(terminal)
                session.flush()     # Assigns ID without committing

                if property_.type_ == "PROPERTY" or property_.type_ == "INSTANCE":
                    property_.type_ = "INSTANCE"
                    session.add(property_)
                    triple = GraphIIT(subject=instance.id, predicate=property_.id, object_=terminal.id)
                    # Add things directly to session, if anything fails whole transaction is aborted
                    session.add(triple)
                else:
                    session.close()
                    raise NotInstanceProperty(type_=prop_name)

    session.commit()
    return instance.id


def delete(id_, type_, session):
    """Delete an Instance and all its relations from DB given id [DELETE]."""
    try:
        rdf_class = session.query(RDFClass).filter(RDFClass.name == type_).one()
    except NoResultFound:
        print(type_)
        raise ClassNotFound(type_=type_)
    try:
        instance = session.query(Instance).filter(
            Instance.id == id_ and type_ == rdf_class.id).one()
    except NoResultFound:
        raise InstanceNotFound(type_=rdf_class.name, id_=id_)

    data_IIT = session.query(triples).filter(triples.GraphIIT.subject == id_).all()
    data_IAC = session.query(triples).filter(triples.GraphIAC.subject == id_).all()
    data_III = session.query(triples).filter(triples.GraphIII.subject == id_).all()

    data = data_III + data_IIT + data_IAC
    for item in data:
        session.delete(item)

    for data in data_IIT:
        terminal = session.query(Terminal).filter(Terminal.id == data.object_).one()
        session.delete(terminal)

    for data in data_III:
        III_instance = session.query(Instance).filter(Instance.id == data.object_).one()
        III_instance_type = session.query(RDFClass).filter(RDFClass.id == III_instance.type_).one()
        # Get the III object type_
        delete(III_instance.id, III_instance_type.name, session=session)

    session.delete(instance)
    session.commit()


def update(id_, type_, object_, session, api_name):
    """Update an object properties based on the given object [PUT]."""
    # Keep the object as fail safe
    instance = get(id_=id_, type_=type_, session=session, api_name=api_name)
    instance.pop("@id")

    # Delete the old object
    delete(id_=id_, type_=type_, session=session)
    # Try inserting new object
    try:
        insert(object_=object_, id_=id_, session=session)
    except Exception as e:
        # Put old object back
        insert(object_=instance, id_=id_, session=session)
        raise e

    get(id_=id_, type_=type_, session=session, api_name=api_name)
    return id_


def get_collection(API_NAME, type_, session):
    """Retrieve a type of collection from the database."""
    collection_template = {
        "@id": "/"+API_NAME+"/" + type_ + "Collection/",
        "@context": None,
        "@type": type_ + "Collection",
        "members": list()
    }
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == type_).one()
    except NoResultFound:
        raise ClassNotFound(type_=type_)

    try:
        instances = session.query(Instance).filter(Instance.type_ == rdf_class.id).all()
    except NoResultFound:
        instances = list()

    for instance_ in instances:
        object_template = {
            "@id": "/"+API_NAME+"/" + type_ + "Collection/" + str(instance_.id),
            "@type": type_
        }
        collection_template["members"].append(object_template)
    return collection_template


def get_single(type_, api_name, session):
    """Get instance of classes with single objects."""
    try:
        rdf_class = session.query(RDFClass).filter(RDFClass.name == type_).one()
    except NoResultFound:
        raise ClassNotFound(type_=type_)

    try:
        instance = session.query(Instance).filter(Instance.type_ == rdf_class.id).all()[-1]
    except (NoResultFound, IndexError, ValueError):
        raise InstanceNotFound(type_=rdf_class.name)
    object_ = get(instance.id, rdf_class.name, session=session, api_name=api_name)

    object_["@id"] = "/"+api_name+"/"+type_

    return object_


def insert_single(object_, session):
    """Insert instance of classes with single objects."""
    try:
        rdf_class = session.query(RDFClass).filter(RDFClass.name == object_["@type"]).one()
    except NoResultFound:
        raise ClassNotFound(type_=object_["@type"])

    try:
        session.query(Instance).filter(Instance.type_ == rdf_class.id).all()[-1]
    except (NoResultFound, IndexError, ValueError):
        return insert(object_, session=session)

    raise InstanceExists(type_=rdf_class.name)


def update_single(object_, session, api_name):
    """Update instance of classes with single objects."""
    try:
        rdf_class = session.query(RDFClass).filter(RDFClass.name == object_["@type"]).one()
    except NoResultFound:
        print("Class not found in update_single")
        raise ClassNotFound(type_=object_["@type"])

    try:
        instance = session.query(Instance).filter(Instance.type_ == rdf_class.id).all()[-1]
    except (NoResultFound, IndexError, ValueError):
        raise InstanceNotFound(type_=rdf_class.name)

    return update(id_=instance.id, type_=object_["@type"], object_=object_, session=session, api_name=api_name)


def delete_single(type_, session):
    """Delete instance of classes with single objects."""
    try:
        rdf_class = session.query(RDFClass).filter(RDFClass.name == type_).one()
    except NoResultFound:
        raise ClassNotFound(type_=type_)

    try:
        instance = session.query(Instance).filter(Instance.type_ == rdf_class.id).all()[-1]
    except (NoResultFound, IndexError, ValueError):
        raise InstanceNotFound(type_=rdf_class.name)

    return delete(instance.id, type_, session=session)
