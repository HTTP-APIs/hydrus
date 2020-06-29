"""
Script to generate the tables in hydrus database based on
resources in the provided API Doc.
"""
import copy
from hydrus.data.db_models import Resource
from hydrus.data.exceptions import (
    ClassNotFound,
    DatabaseConstraintError,
    InstanceExists,
    InstanceNotFound,
    InvalidSearchParameter,
    PropertyNotFound,
    PropertyNotGiven,
)
from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound


def get_type(object_):
    """
    Return the @type of that given object.
    :param object_: Dict containing object properties
    :return: The @type of that object
    """
    return object_["@type"]


def get_database_class(type_):
    """
    Get the sqlalchemy class object from given classname
    :param type_: The @type of a object
    :return: The SQL-Alchemy database class object for that type_
    """
    database_class = Resource.all_database_classes.get(type_, None)
    if database_class is None:
        raise ClassNotFound(type_)
    return database_class


def insert_object(object_, session):
    """
    Insert the object in the database
    :param object_: Dict containing object properties
    :param session: sqlalchemy session
    :return: The ID of the inserted object
    """
    type_ = get_type(object_)
    database_class = get_database_class(type_)
    id_ = object_.get("id", None)
    if (
        id_ is not None and session.query(
            exists().where(database_class.id == id_)).scalar()
    ):
        raise InstanceExists(type_, id_)
    foreign_keys = database_class.__table__.foreign_keys
    for fk in foreign_keys:
        # the name of the column through which this foreign key relationship
        # is being established
        fk_column = fk.info["column_name"]
        try:
            fk_object = object_[fk_column]
        except KeyError as e:
            wrong_property = e.args[0]
            raise PropertyNotGiven(type_=wrong_property)
        # insert the foreign key object
        fk_object_id = insert_object(fk_object, session)
        # put the id of the foreign instance in this table's column
        object_[fk_column] = fk_object_id
    try:
        # remove the @type from object before using the object to make a
        # instance of it using sqlalchemy class
        object_.pop("@type")
        inserted_object = database_class(**object_)
    except TypeError as e:
        # extract the wrong property name from TypeError object
        wrong_property = e.args[0].split("'")[1]
        raise PropertyNotFound(type_=wrong_property)
    try:
        session.add(inserted_object)
        session.commit()
    except Exception as e:
        # catching any database contraint errors
        session.rollback()
        contraint_error = e.orig
        raise DatabaseConstraintError(contraint_error)
    return inserted_object.id


def get_object(query_info, session):
    """
    Get the object from the database
    :param query_info: Dict containing the id and @type of object that has to retrieved
    :param session: sqlalchemy session
    :return: dict of object with its properties
    """
    type_ = query_info["@type"]
    id_ = query_info["id_"]
    database_class = get_database_class(type_)
    try:
        object_ = (
            session.query(database_class)
            .filter(database_class.id == id_)
            .one()
        ).__dict__
    except NoResultFound:
        raise InstanceNotFound(type_=type_, id_=id_)
    # Remove the unnecessary keys from the object retrieved from database
    object_template = copy.deepcopy(object_)
    object_template.pop("_sa_instance_state")
    object_template.pop("id")
    object_template["@type"] = query_info["@type"]
    return object_template


def delete_object(query_info, session):
    """
    Delete the object from the database
    :param query_info: Dict containing the id and @type of object that has to retrieved
    :param session: sqlalchemy session
    """
    type_ = query_info["@type"]
    id_ = query_info["id_"]
    database_class = get_database_class(type_)
    try:
        object_ = (
            session.query(database_class)
            .filter(database_class.id == id_)
            .one()
        )
    except NoResultFound:
        raise InstanceNotFound(type_=type_, id_=id_)
    session.delete(object_)
    try:
        session.commit()
    except Exception:
        session.rollback()


def update_object(object_, query_info, session):
    """
    Update the object from the database
    :param object_: Dict containing updated object properties
    :param query_info: Dict containing the id and @type of object that has to retrieved
    :param session: sqlalchemy session
    :return: the ID of the updated object
    """
    # Keep the object as fail safe
    old_object = get_object(query_info, session)
    # Delete the old object
    delete_object(query_info, session)
    id_ = query_info["id_"]
    # Try inserting new object
    try:
        object_["id"] = id_
        d = insert_object(object_, session)
    except Exception as e:
        # Put old object back
        old_object["id"] = id_
        d = insert_object(old_object, session)
        raise e
    return id_


def all_instances(session, type_):
    database_class = get_database_class(type_)
    try:
        instances = session.query(database_class).all()
        return instances
    except NoResultFound:
        instances = list()
        return instances


def get_all_filtered_instances(session, search_params, type_):
    """Get all the filtered instances of from the database
    based on given query parameters.
    :param session: sqlalchemy scoped session
    :param search_params: Query parameters
    :param type_: @type of object to be deleted
    :return: filtered instances
    """
    database_class = get_database_class(type_)
    try:
        filtered_instances = (
            session.query(database_class).filter_by(**search_params).all()
        )
    except Exception as e:
        # extract the wrong query parameter
        wrong_query_param = e.args[0].split()[-1]
        raise InvalidSearchParameter(wrong_query_param.strip("'"))
    return filtered_instances


def get_single_response(session, type_):
    """
    Get instance of classes with single objects.
    :param session: sqlalchemy scoped session
    :param type_: @type of object to be deleted
    :return: instance
    """
    database_class = get_database_class(type_)
    try:
        instance = session.query(database_class).all()[-1]
    except (NoResultFound, IndexError, ValueError):
        raise InstanceNotFound(type_)

    return instance
