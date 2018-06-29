"""Basic CRUD operations for the server.

    ===============================
    Imports :

    sqlalchemy.orm.with_polymorphic : Load columns for inheriting classes.
    Ref : http://docs.sqlalchemy.org/en/latest/orm/query.html

    sqlalchemy.exists : A convenience method that turns a query into an EXISTS subquery of the form EXISTS (SELECT 1 FROM … WHERE …).
    Ref : http://docs.sqlalchemy.org/en/latest/orm/query.html

    sqlalchemy.orm.exc.NoResultFound : A database result was required but none was found.
    Ref : http://docs.sqlalchemy.org/en/latest/orm/exceptions.html?highlight=result%20found#sqlalchemy.orm.exc.NoResultFound

    sqlalchemy.orm.session.Session : Manages persistence operations for ORM-mapped objects.
    Ref : http://docs.sqlalchemy.org/en/latest/orm/session_api.html?highlight=session#module-sqlalchemy.orm.session

    hydrus.data.db_models.Graph : Model for a graph that store triples of instance from the other models to map relationships.
    hydrus.data.db_models.BaseProperty : Model for Basic Property.
    hydrus.data.db_models.RDFClass : Model for Classes specifically RDF-OWL or RDF-HYDRA classes.
    hydrus.data.db_models.Instance : Model for Object/Resource. Instances are instances of some kind/classes that are served through the API.
    hydrus.data.db_models.Terminal : Model for Terminals which are numbers or string that can be referenced by a Property.
    hydrus.data.db_models.GraphIAC : Graph model for Instance >> AbstractProperty >> Class.
    hydrus.data.db_models.GraphIIT : Graph model for Instance >> InstanceProperty >> Terminal.
    hydrus.data.db_models.GraphIII : Graph model for Instance >> InstanceProperty >> Instance.

    Ref : ./db_models.py

    hydrus.data.exceptions : Contains all exceptions .
    typing : Module which provides support for type hints .

"""

from sqlalchemy.orm import with_polymorphic
from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound
from hydrus.data.db_models import (Graph, BaseProperty, RDFClass, Instance,
                                   Terminal, GraphIAC, GraphIIT, GraphIII)

from hydrus.data.exceptions import (ClassNotFound, InstanceExists, PropertyNotFound,
                                    NotInstanceProperty, NotAbstractProperty,
                                    InstanceNotFound)
# from sqlalchemy.orm.session import Session
from sqlalchemy.orm.scoping import scoped_session
from typing import Dict, Optional, Any, List

triples = with_polymorphic(Graph, '*')
properties = with_polymorphic(BaseProperty, "*")


def get(id_: int, type_: str, api_name: str, session: scoped_session, recursive: bool = False) -> Dict[str, str]:
    """Retrieve an Instance with given ID from the database [GET]."""
    object_template = {
        "@type": "",
    }  # type: Dict[str, Any]
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

    data_IAC = session.query(triples).filter(
        triples.GraphIAC.subject == id_).all()

    data_III = session.query(triples).filter(
        triples.GraphIII.subject == id_).all()

    data_IIT = session.query(triples).filter(
        triples.GraphIIT.subject == id_).all()

    for data in data_IAC:
        prop_name = session.query(properties).filter(
            properties.id == data.predicate).one().name
        class_name = session.query(RDFClass).filter(
            RDFClass.id == data.object_).one().name
        object_template[prop_name] = class_name

    for data in data_III:
        prop_name = session.query(properties).filter(
            properties.id == data.predicate).one().name
        instance = session.query(Instance).filter(
            Instance.id == data.object_).one()
        # Get class name for instance object
        inst_class_name = session.query(RDFClass).filter(
            RDFClass.id == instance.type_).one().name
        # Recursive call should get the instance needed
        object_ = get(id_=instance.id, type_=inst_class_name,
                      session=session, recursive=True, api_name=api_name)
        object_template[prop_name] = object_

    for data in data_IIT:
        prop_name = session.query(properties).filter(
            properties.id == data.predicate).one().name
        terminal = session.query(Terminal).filter(
            Terminal.id == data.object_).one()
        try:
            object_template[prop_name] = terminal.value
        except:
            # If terminal is none
            object_template[prop_name] = ""
    object_template["@type"] = rdf_class.name
    if not recursive:
        object_template["@id"] = "/" + api_name + \
            "/" + type_ + "Collection/" + str(id_)

    return object_template


def insert(object_: Dict[str, Any], session: scoped_session, id_: Optional[int] =None) -> int:
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
                instance_object = session.query(Instance).filter(
                    Instance.id == instance_id).one()

                if property_.type_ == "PROPERTY" or property_.type_ == "INSTANCE":
                    property_.type_ = "INSTANCE"
                    session.add(property_)
                    triple = GraphIII(
                        subject=instance.id, predicate=property_.id, object_=instance_object.id)
                    session.add(triple)
                else:
                    session.close()
                    raise NotInstanceProperty(type_=prop_name)

            # For insertion in IAC
            elif session.query(exists().where(RDFClass.name == str(object_[prop_name]))).scalar():
                if property_.type_ == "PROPERTY" or property_.type_ == "ABSTRACT":
                    property_.type_ = "ABSTRACT"
                    session.add(property_)
                    class_ = session.query(RDFClass).filter(
                        RDFClass.name == object_[prop_name]).one()
                    triple = GraphIAC(subject=instance.id,
                                      predicate=property_.id, object_=class_.id)
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
                    triple = GraphIIT(
                        subject=instance.id, predicate=property_.id, object_=terminal.id)
                    # Add things directly to session, if anything fails whole transaction is aborted
                    session.add(triple)
                else:
                    session.close()
                    raise NotInstanceProperty(type_=prop_name)

    session.commit()
    return instance.id


def insert_multiple(objects_: List[Dict[str, Any]], session: scoped_session, id_: Optional[List[int]] = None):
    """
    Adds a list of object with given ids to the database
    :param objects_: List of dict's to be added to the database
    :param session: scoped session from getSession in utils
    :param id_: optional parameter containing the ids of objects that have to be inserted
    :return:
    """
    # instance list to store instances
    instance_list = list()
    triples_list = list()
    properties_list = list()
    instances = list()
    id_list = id_[0::2]
    print("inside insert multiple")
    # the number of objects would be the same as number of instances
    for index in range(len(objects_)):
        try:
            rdf_class = session.query(RDFClass).filter(
                RDFClass.name == objects_[index]["@type"]).one()
        except NoResultFound:
            raise ClassNotFound(type_=objects_[index]["@type"])
        if id_list[index] is not None:
            if session.query(exists().where(Instance.id == id_list[index])).scalar():
                # TODO handle where intance already exists , if event is fetched later anyways remove this
                raise InstanceExists(type_=rdf_class.name, id_=id_list[index])
            else:
                instance = Instance(id=id_list[index], type_=rdf_class.id)
                instances.append(instance)
        else:
            instance = Instance(type_=rdf_class.id)
            instances.append(instance)


    session.bulk_save_objects(instances)
    session.flush()

    for index in range(len(objects_)):
        for prop_name in objects_[index]:
            if prop_name not in ["@type", "@context"]:
                try:
                    property_ = session.query(properties).filter(
                        properties.name == prop_name).one()
                except NoResultFound:
                    # Adds new Property
                    session.close()
                    raise PropertyNotFound(type_=prop_name)

                # For insertion in III
                if type(objects_[index][prop_name]) == dict:
                    instance_id = insert(objects_[index][prop_name], session=session)
                    instance_object = session.query(Instance).filter(
                        Instance.id == instance_id).one()

                    if property_.type_ == "PROPERTY" or property_.type_ == "INSTANCE":
                        property_.type_ = "INSTANCE"
                        properties_list.append(property_)
                        triple = GraphIII(
                            subject=instances[index].id, predicate=property_.id, object_=instance_object.id)
                        triples_list.append(triple)
                    else:
                        session.close()
                        raise NotInstanceProperty(type_=prop_name)

                # For insertion in IAC
                elif session.query(exists().where(RDFClass.name == str(objects_[index][prop_name]))).scalar():
                    if property_.type_ == "PROPERTY" or property_.type_ == "ABSTRACT":
                        property_.type_ = "ABSTRACT"
                        properties_list.append(property_)
                        class_ = session.query(RDFClass).filter(
                            RDFClass.name == objects_[index][prop_name]).one()
                        triple = GraphIAC(subject=instances[index].id,
                                          predicate=property_.id, object_=class_.id)
                        triples_list.append(triple)

                    else:
                        session.close()
                        raise NotAbstractProperty(type_=prop_name)

                # For insertion in IIT
                else:
                    terminal = Terminal(value=objects_[index][prop_name])
                    session.add(terminal)
                    session.flush()     # Assigns ID without committing

                    if property_.type_ == "PROPERTY" or property_.type_ == "INSTANCE":
                        property_.type_ = "INSTANCE"
                        properties_list.append(property_)
                        triple = GraphIIT(
                            subject=instances[index].id, predicate=property_.id, object_=terminal.id)
                        # Add things directly to session, if anything fails whole transaction is aborted
                        triples_list.append(triple)
                    else:
                        session.close()
                        raise NotInstanceProperty(type_=prop_name)
    #session.bulk_save_objects(properties_list)
    #session.bulk_save_objects(triples_list)

    session.commit()
    return 0




def delete(id_: int, type_: str, session: scoped_session) -> None:
    """Delete an Instance and all its relations from DB given id [DELETE]."""
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == type_).one()
    except NoResultFound:
        print(type_)
        raise ClassNotFound(type_=type_)
    try:
        instance = session.query(Instance).filter(
            Instance.id == id_ and type_ == rdf_class.id).one()
    except NoResultFound:
        raise InstanceNotFound(type_=rdf_class.name, id_=id_)

    data_IIT = session.query(triples).filter(
        triples.GraphIIT.subject == id_).all()
    data_IAC = session.query(triples).filter(
        triples.GraphIAC.subject == id_).all()
    data_III = session.query(triples).filter(
        triples.GraphIII.subject == id_).all()

    data = data_III + data_IIT + data_IAC
    for item in data:
        session.delete(item)

    for data in data_IIT:
        terminal = session.query(Terminal).filter(
            Terminal.id == data.object_).one()
        session.delete(terminal)

    for data in data_III:
        III_instance = session.query(Instance).filter(
            Instance.id == data.object_).one()
        III_instance_type = session.query(RDFClass).filter(
            RDFClass.id == III_instance.type_).one()
        # Get the III object type_
        delete(III_instance.id, III_instance_type.name, session=session)

    session.delete(instance)
    session.commit()


def update(id_: int, type_: str, object_: Dict[str, str], session: scoped_session, api_name: str) -> int:
    """Update an object properties based on the given object [PUT]."""
    # Keep the object as fail safe
    instance = get(id_=id_, type_=type_, session=session, api_name=api_name)
    instance.pop("@id")

    # Delete the old object
    delete(id_=id_, type_=type_, session=session)
    # Try inserting new object
    try:
        insert(object_=object_, id_=id_, session=session)
    except (ClassNotFound, InstanceExists, PropertyNotFound) as e:
        # Put old object back
        insert(object_=instance, id_=id_, session=session)
        raise e

    get(id_=id_, type_=type_, session=session, api_name=api_name)
    return id_


def get_collection(API_NAME: str, type_: str, session: scoped_session) -> Dict[str, Any]:
    """Retrieve a type of collection from the database."""
    collection_template = {
        "@id": "/" + API_NAME + "/" + type_ + "Collection/",
        "@context": None,
        "@type": type_ + "Collection",
        "members": list()
    }  # type: Dict[str, Any]
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == type_).one()
    except NoResultFound:
        raise ClassNotFound(type_=type_)

    try:
        instances = session.query(Instance).filter(
            Instance.type_ == rdf_class.id).all()
    except NoResultFound:
        instances = list()

    for instance_ in instances:
        object_template = {
            "@id": "/" + API_NAME + "/" + type_ + "Collection/" + str(instance_.id),
            "@type": type_
        }
        collection_template["members"].append(object_template)
    return collection_template


def get_single(type_: str, api_name: str, session: scoped_session) -> Dict[str, Any]:
    """Get instance of classes with single objects."""
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == type_).one()
    except NoResultFound:
        raise ClassNotFound(type_=type_)

    try:
        instance = session.query(Instance).filter(
            Instance.type_ == rdf_class.id).all()[-1]
    except (NoResultFound, IndexError, ValueError):
        raise InstanceNotFound(type_=rdf_class.name)
    object_ = get(instance.id, rdf_class.name,
                  session=session, api_name=api_name)

    object_["@id"] = "/" + api_name + "/" + type_

    return object_


def insert_single(object_: Dict[str, Any], session: scoped_session) -> Any:
    """Insert instance of classes with single objects."""
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == object_["@type"]).one()
    except NoResultFound:
        raise ClassNotFound(type_=object_["@type"])

    try:
        session.query(Instance).filter(
            Instance.type_ == rdf_class.id).all()[-1]
    except (NoResultFound, IndexError, ValueError):
        return insert(object_, session=session)

    raise InstanceExists(type_=rdf_class.name)


def update_single(object_: Dict[str, Any], session: scoped_session, api_name: str) -> int:
    """Update instance of classes with single objects."""
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == object_["@type"]).one()
    except NoResultFound:
        print("Class not found in update_single")
        raise ClassNotFound(type_=object_["@type"])

    try:
        instance = session.query(Instance).filter(
            Instance.type_ == rdf_class.id).all()[-1]
    except (NoResultFound, IndexError, ValueError):
        raise InstanceNotFound(type_=rdf_class.name)

    return update(id_=instance.id, type_=object_["@type"], object_=object_, session=session, api_name=api_name)


def delete_single(type_: str, session: scoped_session) -> None:
    """Delete instance of classes with single objects."""
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == type_).one()
    except NoResultFound:
        raise ClassNotFound(type_=type_)

    try:
        instance = session.query(Instance).filter(
            Instance.type_ == rdf_class.id).all()[-1]
    except (NoResultFound, IndexError, ValueError):
        raise InstanceNotFound(type_=rdf_class.name)

    return delete(instance.id, type_, session=session)






def update_multiple():
    pass
def delete_multiple():
    pass