"""
Script to generate the tables in hydrus database based on
resources in the provided API Doc.
"""
import copy
import uuid
from dateutil import parser
from hydrus.data.db_models import Resource
from hydrus.data.exceptions import (
    ClassNotFound,
    InstanceExists,
    InstanceNotFound,
    InvalidSearchParameter,
    PropertyNotFound,
    PropertyNotGiven,
    MemberInstanceNotFound,
    InvalidDateTimeFormat
)
from sqlalchemy import exists
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.exc import NoResultFound
from hydra_python_core.doc_writer import HydraDoc
from typing import Dict, Any


def get_type(object_: Dict[str, Any]) -> str:
    """
    Return the @type of that given object.
    :param object_: Dict containing object properties
    :return: The @type of that object
    """
    try:
        type_ = object_["@type"]
    except TypeError:
        raise ClassNotFound(object_)
    return type_


def get_modified_object(object_: Dict[str, Any], doc: HydraDoc, path: str) -> Dict[str, Any]:
    """
    Return the object after modifying properties.
    :param object_: Dict containing object properties
    :param doc: HydraDoc object
    :param path: Path of the Class or Collection
    :return: object_ containing properties
    """
    class_ = doc.parsed_classes[path]
    properties = class_["class"].supportedProperty
    datetimefields = []
    for prop in properties:
        kwargs = getattr(prop, 'kwargs', None)
        range = kwargs.get('range')
        title = getattr(prop, 'title')
        if range is not None:
            if "dateTime" in range:
                datetimefield = title
                datetimefields.append(datetimefield)
    if len(datetimefields) != 0:
        for field in datetimefields:
            try:
                datetime_value = object_.get(field)
                dt_object = parser.isoparse(datetime_value)
                object_[field] = dt_object
            except ValueError:
                # Error is raised in case of invalid datetime format
                raise InvalidDateTimeFormat(field)
            except TypeError:
                # In case, when datetime field isn't a string
                datetime_value = object_.get(field)
                object_[field] = datetime_value
    return object_


def get_database_class(type_: str):
    """
    Get the sqlalchemy class object from given classname
    :param type_: The @type of a object
    :return: The SQL-Alchemy database class object for that type_
    """
    database_class = Resource.all_database_classes.get(type_, None)
    if database_class is None:
        raise ClassNotFound(type_)
    return database_class


def insert_object(
    doc_: HydraDoc, object_: Dict[str, Any], session: scoped_session, collection: bool = False
) -> str:
    """
    Insert the object in the database
    :param doc_: HydraDoc object
    :param object_: Dict containing object properties
    :param session: sqlalchemy session
    :return: The ID of the inserted object
    """
    type_ = get_type(object_)
    database_class = get_database_class(type_)
    id_ = object_.get("id", None)
    if collection:
        # if type_ is of a collection class
        members = object_["members"]
        collection_id = id_ if id_ else str(uuid.uuid4())
        for member in members:
            # add all the members of that collection
            inserted_object = database_class(
                members=member["id_"],
                collection_id=collection_id,
                member_type=member["@type"],
            )
            try:
                session.add(inserted_object)
                session.commit()
            except InvalidRequestError:
                session.rollback()
            except IntegrityError:
                session.rollback()
                member_type_ = member["@type"]
                member_id_ = member["id_"]
                raise InstanceExists(member_type_, member_id_)
        return collection_id
    else:
        # when type_ is of a non-collection class
        if (
            id_ is not None and
            session.query(exists().where(database_class.id == id_)).scalar()
        ):
            raise InstanceExists(type_, id_)
        foreign_keys = database_class.__table__.foreign_keys
        for fk in foreign_keys:
            # the name of the column through which this foreign key relationship
            # is being established
            fk_column = fk.info["column_name"]
            try:
                fk_object = object_[fk_column]
                fk_object_path = fk_object.get('@type')
                fk_object = get_modified_object(fk_object, doc_, fk_object_path)
            except KeyError as e:
                wrong_property = e.args[0]
                raise PropertyNotGiven(type_=wrong_property)
            # insert the foreign key object
            fk_object_id = insert_object(doc_, fk_object, session)
            # put the id of the foreign instance in this table's column
            object_[fk_column] = fk_object_id
        try:
            # remove the @type from object before using the object to make a
            # instance of it using sqlalchemy class
            object_path = object_.get('@type')
            object_ = get_modified_object(object_, doc_, object_path)
            object_.pop("@type")
            inserted_object = database_class(**object_)
        except TypeError as e:
            # extract the wrong property name from TypeError object
            wrong_property = e.args[0].split("'")[1]
            raise PropertyNotFound(type_=wrong_property)
        try:
            session.add(inserted_object)
            session.commit()
        except InvalidRequestError:
            session.rollback()

        return inserted_object.id


def get_object(
    query_info: Dict[str, str], session: scoped_session, collection: bool = False
) -> Dict[str, str]:
    """
    Get the object from the database
    :param query_info: Dict containing the id and @type of object that has to retrieved
    :param session: sqlalchemy session
    :param collection: True if the type_ is of a collection, False for any other class
    :return: dict of object with its properties
    """
    type_ = query_info["@type"]
    id_ = query_info["id_"]
    database_class = get_database_class(type_)
    if collection:
        objects = (
            session.query(database_class.members, database_class.member_type)
            .filter(database_class.collection_id == id_)
            .all()
        )
        if len(objects) == 0:
            raise InstanceNotFound(type_=type_, id_=id_)
        object_template = {}
        object_template["@type"] = query_info["@type"]
        object_template["members"] = objects
        return object_template
    else:
        try:
            object_ = (
                session.query(database_class).filter(database_class.id == id_).one()
            ).__dict__
        except NoResultFound:
            raise InstanceNotFound(type_=type_, id_=id_)
        # Remove the unnecessary keys from the object retrieved from database
        object_template = copy.deepcopy(object_)
        object_template.pop("_sa_instance_state")
        object_template.pop("id")
        object_template["@type"] = query_info["@type"]
        return object_template


def delete_object(
    query_info: Dict[str, str], session: scoped_session, collection: bool = False
) -> None:
    """
    Delete the object from the database
    :param query_info: Dict containing the id and @type of object that has to retrieved
    :param session: sqlalchemy session
    :param collection: True if the type_ is of a collection, False for any other class
    """
    type_ = query_info["@type"]
    id_ = query_info["id_"]
    database_class = get_database_class(type_)
    if collection:
        try:
            objects = (
                session.query(database_class).filter_by(collection_id=id_).delete()
            )
        except NoResultFound:
            raise InstanceNotFound(type_=type_, id_=id_)
        try:
            session.commit()
        except InvalidRequestError:
            session.rollback()
        return id_
    else:
        try:
            object_ = (
                session.query(database_class).filter(database_class.id == id_).one()
            )
        except NoResultFound:
            raise InstanceNotFound(type_=type_, id_=id_)
        session.delete(object_)
        try:
            session.commit()
        except InvalidRequestError:
            session.rollback()


def update_object(
    doc_: HydraDoc,
    object_: Dict[str, Any],
    query_info: Dict[str, str],
    session: scoped_session,
    collection: bool = False,
) -> str:
    """
    Update the object from the database
    :param doc_: HydraDoc object
    :param object_: Dict containing updated object properties
    :param query_info: Dict containing the id and @type of object that has to retrieved
    :param session: sqlalchemy session
    :return: the ID of the updated object
    """
    # Keep the object as fail safe
    old_object = get_object(query_info, session, collection)
    # Delete the old object
    delete_object(query_info, session, collection)
    id_ = query_info["id_"]
    # Try inserting new object
    try:
        object_["id"] = id_
        d = insert_object(doc_, object_, session, collection)
    except Exception as e:
        # Put old object back
        old_object["id"] = id_
        d = insert_object(doc_, old_object, session, collection)
        raise e
    return id_


def get_collection_member(
    query_info: Dict[str, str], session: scoped_session
) -> Dict[str, str]:
    """
    Get member from a collection
    :param query_info: Dict containing the ids and @type of object that has to retrieved
    :param session: sqlalchemy session
    :return: dict of object with its properties
    """
    type_ = query_info["@type"]
    collection_id = query_info["collection_id"]
    member_id = query_info["member_id"]
    database_class = get_database_class(type_)
    objects = (
        session.query(database_class.members, database_class.member_type)
        .filter(
            database_class.collection_id == collection_id,
            database_class.members == member_id,
        )
        .all()
    )
    if len(objects) == 0:
        raise MemberInstanceNotFound(
            type_=type_, collection_id_=collection_id, member_id_=member_id
        )
    object_template = {}
    object_template["@type"] = query_info["@type"]
    object_template["members"] = objects
    return object_template


def delete_collection_member(
    query_info: Dict[str, str], session: scoped_session
) -> None:
    """
    Delete the object from the collection in database
    :param query_info: Dict containing the id and @type of object that has to retrieved
    :param session: sqlalchemy session
    """
    type_ = query_info["@type"]
    member_id = query_info["member_id"]
    collection_id = query_info["collection_id"]
    database_class = get_database_class(type_)
    objects = (
        session.query(database_class)
        .filter(
            database_class.collection_id == collection_id,
            database_class.members == member_id,
        )
        .delete()
    )
    if objects == 0:
        raise MemberInstanceNotFound(
            type_=type_, collection_id_=collection_id, member_id_=member_id
        )
    try:
        session.commit()
    except InvalidRequestError:
        session.rollback()
    return collection_id


def get_all_filtered_instances(
    session: scoped_session,
    search_params: Dict[str, Any],
    type_: str,
    collection: bool = False,
):
    """Get all the filtered instances of from the database
    based on given query parameters.
    :param session: sqlalchemy scoped session
    :param search_params: Query parameters
    :param type_: @type of object to be deleted
    :param collection: True if the type_ is of a collection, False for any other class
    :return: filtered instances
    """
    database_class = get_database_class(type_)
    if collection:
        query = session.query(database_class.collection_id.label("id")).distinct()
    else:
        query = session.query(database_class)
        for param, param_value in search_params.items():
            # nested param
            if type(param_value) is dict:
                foreign_keys = database_class.__table__.foreign_keys
                for fk in foreign_keys:
                    if fk.info["column_name"] == param:
                        fk_table_name = fk.column.table.name
                        continue
                nested_param_db_class = get_database_class(fk_table_name)
                # build query
                for attr, value in param_value.items():
                    query = query.join(nested_param_db_class)
                    try:
                        query = query.filter(
                            getattr(nested_param_db_class, attr) == value
                        )
                    except AttributeError:
                        raise InvalidSearchParameter(f"{param}[{attr}]")
            else:
                value = search_params[param]
                try:
                    query = query.filter(getattr(database_class, param) == value)
                except AttributeError:
                    raise InvalidSearchParameter(f"{param}")

    filtered_instances = query.all()
    return filtered_instances


def get_single_response(session: scoped_session, type_: str):
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
