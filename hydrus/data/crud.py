"""Basic CRUD operations for the server.

    ===============================
    Imports :

    sqlalchemy.orm.with_polymorphic : Load columns for inheriting classes.
    Ref : http://docs.sqlalchemy.org/en/latest/orm/query.html

    sqlalchemy.exists : A convenience method that turns a query into an EXISTS subquery
    of the form EXISTS (SELECT 1 FROM … WHERE …).
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

"""  # nopep8

from sqlalchemy.orm import with_polymorphic
from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound
from hydrus.data.db_models import (Graph, BaseProperty, RDFClass, Instance,
                                   Terminal, GraphIAC, GraphIIT, GraphIII)
from hydrus.utils import get_doc

from hydrus.data.exceptions import (
    ClassNotFound,
    InstanceExists,
    PropertyNotFound,
    NotInstanceProperty,
    NotAbstractProperty,
    InstanceNotFound)
# from sqlalchemy.orm.session import Session
from sqlalchemy.orm.scoping import scoped_session
from typing import Dict, Optional, Any, List

triples = with_polymorphic(Graph, '*')
properties = with_polymorphic(BaseProperty, "*")


def get(id_: str, type_: str, api_name: str, session: scoped_session,
        path: str = None) -> Dict[str, str]:
    """Retrieve an Instance with given ID from the database [GET].
    :param id_: id of object to be fetched
    :param type_: type of object
    :param api_name: name of api specified while starting server
    :param session: sqlalchemy scoped session
    :param path: endpoint
    :return: response to the request


    Raises:
        ClassNotFound: If the `type_` is not a valid/defined RDFClass.
        InstanceNotFound: If no Instance of the 'type_` class if found.

    """
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
        doc = get_doc()
        nested_class_path = ""
        for collection in doc.collections:
            if doc.collections[collection]["collection"].class_.path == inst_class_name:
                nested_class_path = doc.collections[collection]["collection"].path
                object_template[prop_name] = "/{}/{}/{}".format(
                    api_name, nested_class_path, instance.id)
                break

        if nested_class_path == "":
            object_template[prop_name] = "/{}/{}/".format(
                api_name, inst_class_name)

    for data in data_IIT:
        prop_name = session.query(properties).filter(
            properties.id == data.predicate).one().name
        terminal = session.query(Terminal).filter(
            Terminal.id == data.object_).one()
        try:
            object_template[prop_name] = terminal.value
        except BaseException:
            # If terminal is none
            object_template[prop_name] = ""
    object_template["@type"] = rdf_class.name

    if path is not None:
        object_template["@id"] = "/{}/{}Collection/{}".format(
            api_name, path, id_)
    else:
        object_template["@id"] = "/{}/{}Collection/{}".format(
            api_name, type_, id_)

    return object_template


def insert(object_: Dict[str, Any], session: scoped_session,
           id_: Optional[str] = None) -> str:
    """Insert an object to database [POST] and returns the inserted object.
    :param object_: object to be inserted
    :param session: sqlalchemy scoped session
    :param id_: id of the object to be inserted (optional param)
    :return: ID of object inserted


    Raises:
        ClassNotFound: If `object_["@type"] is not a valid/defined RDFClass.
        InstanceExists: If an Instance `id_` already exists.
        PropertyNotFound: If any property name of `object_` other than `@type` or `@context`
            is not a valid/defined property.
        NotInstanceProperty: If any property of `object_` is a dictionary but
            not an Instance property
        NotAbstractProperty: If any property of `object_` is a
            valid/defined RDFClass but is not a dictionary neither an Abstract Property

    """
    rdf_class = None
    instance = None
    # Check for class in the begging
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == object_["@type"]).one()
    except NoResultFound:
        raise ClassNotFound(type_=object_["@type"])
    if id_ is not None and session.query(exists().where(Instance.id == id_)).scalar():
        raise InstanceExists(type_=rdf_class.name, id_=id_)
    elif id_ is not None:
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
            if isinstance(object_[prop_name], dict):
                instance_id = insert(object_[prop_name], session=session)
                instance_object = session.query(Instance).filter(
                    Instance.id == instance_id).one()
                if property_.type_ == "PROPERTY" or property_.type_ == "INSTANCE":
                    property_.type_ = "INSTANCE"
                    session.add(property_)
                    triple = GraphIII(
                        subject=instance.id,
                        predicate=property_.id,
                        object_=instance_object.id)
                    session.add(triple)
                else:
                    session.close()
                    raise NotInstanceProperty(type_=prop_name)

            # For insertion in IAC
            elif session.query(exists().where(RDFClass.name == str(object_[prop_name]))).scalar() \
                    and property_.type_ == "PROPERTY" or property_.type_ == "ABSTRACT":
                property_.type_ = "ABSTRACT"
                session.add(property_)
                class_ = session.query(RDFClass).filter(
                    RDFClass.name == object_[prop_name]).one()
                triple = GraphIAC(
                    subject=instance.id,
                    predicate=property_.id,
                    object_=class_.id)
                session.add(triple)
            elif session.query(exists().where(RDFClass.name == str(object_[prop_name]))).scalar():
                session.close()
                raise NotAbstractProperty(type_=prop_name)

            # For insertion in IIT
            else:
                terminal = Terminal(value=object_[prop_name])
                session.add(terminal)
                session.flush()  # Assigns ID without committing

                if property_.type_ == "PROPERTY" or property_.type_ == "INSTANCE":
                    property_.type_ = "INSTANCE"
                    session.add(property_)
                    triple = GraphIIT(
                        subject=instance.id,
                        predicate=property_.id,
                        object_=terminal.id)
                    # Add things directly to session, if anything fails whole
                    # transaction is aborted
                    session.add(triple)
                else:
                    session.close()
                    raise NotInstanceProperty(type_=prop_name)

    session.commit()
    return instance.id


def insert_multiple(objects_: List[Dict[str,
                                        Any]],
                    session: scoped_session,
                    id_: Optional[str] = "") -> List[int]:
    """
    Adds a list of object with given ids to the database
    :param objects_: List of dict's to be added to the database
    :param session: scoped session from getSession in utils
    :param id_: optional parameter containing the ids of objects that have to be inserted
    :return: Ids that have been inserted

    Raises:
        ClassNotFound: If any dict of `objects_` is not a valid/defined RDFClass.
        InstanceExists: If an Instance with same id already exists.
        PropertyNotFound: If for any dict in 'objects_' if any property is not
            a valid/defined property.
        NotAnInstanceProperty: If any property of a dict in `object_` is a dictionary but
            not an Instance property
        NotAnAbstractProperty: If any property of a dict in `object_` is a
            valid/defined RDFClass but is not a dictionary neither an Abstract Property

    """
    # instance list to store instances
    instance_list = list()
    triples_list = list()
    properties_list = list()
    instances = list()
    id_list = id_.split(',')
    instance_id_list = list()

    # the number of objects would be the same as number of instances
    for index in range(len(objects_)):
        try:
            rdf_class = session.query(RDFClass).filter(
                RDFClass.name == objects_[index]["@type"]).one()
        except NoResultFound:
            raise ClassNotFound(type_=objects_[index]["@type"])
        if index in range(len(id_list)) and id_list[index] != "":
            if session.query(
                    exists().where(
                        Instance.id == id_list[index])).scalar():
                print(session.query(
                    exists().where(
                        Instance.id == id_list[index])))
                # TODO handle where intance already exists , if instance is
                # fetched later anyways remove this
                raise InstanceExists(type_=rdf_class.name, id_=id_list[index])
            else:
                instance = Instance(id=id_list[index], type_=rdf_class.id)
                instances.append(instance)
        else:
            instance = Instance(type_=rdf_class.id)
            instances.append(instance)

    session.add_all(instances)
    session.flush()
    for i in range(len(instances)):
        instance_id_list.append(instances[i].id)

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
                if isinstance(objects_[index][prop_name], dict):
                    instance_id = insert(
                        objects_[index][prop_name], session=session)
                    instance_object = session.query(Instance).filter(
                        Instance.id == instance_id).one()

                    if property_.type_ == "PROPERTY" or property_.type_ == "INSTANCE":
                        property_.type_ = "INSTANCE"
                        properties_list.append(property_)
                        triple = GraphIII(
                            subject=instances[index].id,
                            predicate=property_.id,
                            object_=instance_object.id)
                        triples_list.append(triple)
                    else:
                        session.close()
                        raise NotInstanceProperty(type_=prop_name)

                # For insertion in IAC
                elif session.query(
                        exists().where(RDFClass.name == str(objects_[index][prop_name]))).scalar():
                    if property_.type_ == "PROPERTY" or property_.type_ == "ABSTRACT":
                        property_.type_ = "ABSTRACT"
                        properties_list.append(property_)
                        class_ = session.query(RDFClass).filter(
                            RDFClass.name == objects_[index][prop_name]).one()
                        triple = GraphIAC(
                            subject=instances[index].id,
                            predicate=property_.id,
                            object_=class_.id)
                        triples_list.append(triple)

                    else:
                        session.close()
                        raise NotAbstractProperty(type_=prop_name)

                # For insertion in IIT
                else:
                    terminal = Terminal(value=objects_[index][prop_name])
                    session.add(terminal)
                    session.flush()  # Assigns ID without committing

                    if property_.type_ == "PROPERTY" or property_.type_ == "INSTANCE":
                        property_.type_ = "INSTANCE"
                        properties_list.append(property_)
                        triple = GraphIIT(
                            subject=instances[index].id,
                            predicate=property_.id,
                            object_=terminal.id)
                        # Add things directly to session, if anything fails
                        # whole transaction is aborted
                        triples_list.append(triple)
                    else:
                        session.close()
                        raise NotInstanceProperty(type_=prop_name)
    session.bulk_save_objects(properties_list)
    session.bulk_save_objects(triples_list)
    session.commit()
    return instance_id_list


def delete(id_: str, type_: str, session: scoped_session) -> None:
    """Delete an Instance and all its relations from DB given id [DELETE].
    :param id_: id of object to be deleted
    :param type_: type of object to be deleted
    :param session: sqlalchemy scoped session

    Raises:
        ClassNotFound: If `type_` does not represent a valid/defined RDFClass.
        InstanceNotFound: If no instace of type `type_` with id `id_` exists.

    """
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == type_).one()
    except NoResultFound:
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


def delete_multiple(
        id_: List[int],
        type_: str,
        session: scoped_session) -> None:
    """
    To delete multiple rows in a single request
    :param id_: list of ids for objects to be deleted\
    :param type_: type of object to be deleted
    :param session: sqlalchemy scoped session

    Raises:
        ClassNotFound: If `type_` does not represent a valid/defined RDFClass.
        InstanceNotFound: If any instance with type 'type_' and any id in 'id_' list
            does not exist.

    """
    id_ = id_.split(',')
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == type_).one()
    except NoResultFound:
        raise ClassNotFound(type_=type_)

    instances = list()
    data_III = list()
    data_IAC = list()
    data_IIT = list()

    for index in id_:
        try:
            instance = session.query(Instance).filter(
                Instance.id == index and type_ == rdf_class.id).one()
            instances.append(instance)
        except NoResultFound:
            raise InstanceNotFound(type_=rdf_class.name, id_=index)
        data_IIT += session.query(triples).filter(
            triples.GraphIIT.subject == index).all()
        data_IAC += session.query(triples).filter(
            triples.GraphIAC.subject == index).all()
        data_III += session.query(triples).filter(
            triples.GraphIII.subject == index).all()

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
    for instance in instances:
        session.delete(instance)
    session.commit()


def update(id_: str,
           type_: str,
           object_: Dict[str,
                         str],
           session: scoped_session,
           api_name: str,
           path: str = None) -> str:
    """Update an object properties based on the given object [PUT].
    :param id_: if of object to be updated
    :param type_: type of object to be updated
    :param object_: object that has to be inserted
    :param session: sqlalchemy scoped session
    :param api_name: api name specified while starting server
    :param path: endpoint
    :return: id of updated object
    """
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

    get(id_=id_, type_=type_, session=session, api_name=api_name, path=path)
    return id_


def get_collection(API_NAME: str,
                   type_: str,
                   session: scoped_session,
                   path: str = None) -> Dict[str,
                                             Any]:
    """Retrieve a type of collection from the database.
    :param API_NAME: api name specified while starting server
    :param type_: type of object to be updated
    :param session: sqlalchemy scoped session
    :param path: endpoint
    :return: response containing all the objects of that particular type_

    Raises:
        ClassNotFound: If `type_` does not represt a valid/defined RDFClass.

    """
    if path is not None:
        collection_template = {
            "@id": "/{}/{}/".format(API_NAME, path),
            "@context": None,
            "@type": "{}Collection".format(type_),
            "members": list()
        }  # type: Dict[str, Any]
    else:
        collection_template = {
            "@id": "/{}/{}Collection/".format(API_NAME, type_),
            "@context": None,
            "@type": "{}Collection".format(type_),
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
        if path is not None:
            object_template = {
                "@id": "/{}/{}/{}".format(API_NAME, path, instance_.id),
                "@type": type_
            }
        else:
            object_template = {
                "@id": "/{}/{}Collection/{}".format(API_NAME, type_, instance_.id), "@type": type_}
        collection_template["members"].append(object_template)
    return collection_template


def get_single(type_: str, api_name: str, session: scoped_session,
               path: str = None) -> Dict[str, Any]:
    """Get instance of classes with single objects.
    :param type_: type of object to be updated
    :param api_name: api name specified while starting server
    :param session: sqlalchemy scoped session
    :param path: endpoint
    :return: response containing information about a single object

    Raises:
        ClassNotFound: If `type_` does not represt a valid/defined RDFClass.
        InstanceNotFound: If no Instance with type `type_` exists.

    """
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
                  session=session, api_name=api_name, path=path)
    if path is not None:
        object_["@id"] = "/{}/{}".format(api_name, path)
    else:
        object_["@id"] = "/{}/{}".format(api_name, type_)
    return object_


def insert_single(object_: Dict[str, Any], session: scoped_session) -> Any:
    """Insert instance of classes with single objects.
    :param object_: object to be inserted
    :param session: sqlalchemy scoped session
    :return:

    Raises:
        ClassNotFound: If `type_` does not represt a valid/defined RDFClass.
        Instance: If an Instance of type `type_` already exists.

    """
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


def update_single(object_: Dict[str,
                                Any],
                  session: scoped_session,
                  api_name: str,
                  path: str = None) -> int:
    """Update instance of classes with single objects.
    :param object_: new object
    :param session: sqlalchemy scoped session
    :param api_name: api name specified while starting server
    :param path: endpoint
    :return: id of the updated object

    Raises:
        ClassNotFound: If `object['@type']` does not represt a valid/defined RDFClass.
        InstanceNotFound: If no Instance of the class exists.

    """
    try:
        rdf_class = session.query(RDFClass).filter(
            RDFClass.name == object_["@type"]).one()
    except NoResultFound:
        raise ClassNotFound(type_=object_["@type"])

    try:
        instance = session.query(Instance).filter(
            Instance.type_ == rdf_class.id).all()[-1]
    except (NoResultFound, IndexError, ValueError):
        raise InstanceNotFound(type_=rdf_class.name)

    return update(
        id_=instance.id,
        type_=object_["@type"],
        object_=object_,
        session=session,
        api_name=api_name,
        path=path)


def delete_single(type_: str, session: scoped_session) -> None:
    """Delete instance of classes with single objects.
    :param type_: type of object to be deleted
    :param session: sqlalchemy scoped session
    :return: None

    Raises:
        ClassNotFound: If `type_` does not represt a valid/defined RDFClass.
        InstanceNotFound: If no Instance of the class exists.

    """
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
