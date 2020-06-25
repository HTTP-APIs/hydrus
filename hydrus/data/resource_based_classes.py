"""
Script to generate the tables in hydrus database based on
resources in the provided API Doc.
"""
from hydrus.data.db_models import Resource
from hydrus.data.exceptions import (ClassNotFound, DatabaseConstraintError,
                                    InstanceExists, InstanceNotFound,
                                    InvalidSearchParameter, PropertyNotFound)
from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound


def get_type(object_):
    """Return the @type of that given object"""
    return object_["@type"]


def get_database_class(type_):
    """Get the sqlalchemy class object from given classname"""
    database_class = Resource.all_database_classes.get(type_, None)
    if database_class is None:
        raise ClassNotFound(type_)
    return database_class


def insert_object(object_, session):
    """Insert the object in the database"""
    type_ = get_type(object_)
    database_class = get_database_class(type_)
    id_ = object_.get("id", None)
    # remove the @type from object before using the object to make a
    # instance of it using sqlalchemy class
    object_.pop("@type")
    if (
        id_ is not None
        and session.query(exists().where(database_class.id == id_)).scalar()
    ):
        raise InstanceExists(type_, id_)
    try:
        inserted_object = database_class(**object_)
    except TypeError as e:
        # extract the wrong property name from TypeError object
        wrong_propery = e.args[0].split("'")[1]
        raise PropertyNotFound(type_=wrong_propery)
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
    """Get the object from the database"""
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
    object_.pop("_sa_instance_state")
    object_.pop("id")
    object_["@type"] = query_info["@type"]
    return object_


def delete_object(query_info, session):
    """Delete the object from the database"""
    type_ = query_info["@type"]
    id_ = query_info["id_"]
    database_class = get_database_class(type_)
    id_ = query_info["id_"]
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
    """Update the object from the database"""
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
    :param type_: type of object to be deleted
    :return: filtered instances
    """
    database_class = get_database_class(type_)
    try:
        filtered_instances = (
            session.query(database_class).filter_by(**search_params).all()
        )
    except Exception as e:
        # extract the wrong query parameter
        import pdb

        pdb.set_trace()
        wrong_query_param = e.args[0].split()[-1]
        raise InvalidSearchParameter(wrong_query_param.strip("'"))
    return filtered_instances