"""
Script to generate the tables in hydrus database based on
resources in the provided API Doc.
"""
import sqlite3
import uuid
from sqlite3 import Connection as SQLite3Connection

from hydra_python_core import doc_maker
from hydrus.conf import APIDOC_OBJ
from hydrus.data.doc_parse import get_classes
from hydrus.data.exceptions import (
    ClassNotFound,
    PropertyNotFound,
    InstanceNotFound,
    DatabaseConstraintError,
)
from sqlalchemy import Column, ForeignKey, String, create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

serverurl = "http://localhost"
port = 8080
HYDRUS_SERVER_URL = f"{serverurl}:{str(port)}/"
API_NAME = "serverapi"
apidoc = doc_maker.create_doc(APIDOC_OBJ, HYDRUS_SERVER_URL, API_NAME)

classes = get_classes(apidoc.generate())
class_names = []


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


engine = create_engine("sqlite:///database4.db")
Base = declarative_base()
# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()


class Resource:
    # TODO: Look for a better way to store the sql alchemy class for each resource
    all_database_classes = {}

    def __init__(self, resource):
        self._resource = resource

    @property
    def name(self):
        # split the classname at "vocab:" to get the class name
        return self._resource["@id"].split("vocab:")[1]

    @property
    def resource(self):
        return self._resource

    @property
    def supported_properties(self):
        return self._resource["supportedProperty"]

    def get_attr_dict(self):
        attr_dict = {
            "__tablename__": self.name,
            "id": Column(
                String,
                default=lambda: str(uuid.uuid4()),
                unique=True,
                primary_key=True,
            ),
        }
        for supported_property in self.supported_properties:
            title = supported_property["title"]
            link = supported_property["property"]
            if type(link) is not dict:
                if "vocab:" in link:
                    # if vocab: is in the link, it implies that the link is pointing to
                    # another resource in the same ApiDoc, hence make it a Foreign Key
                    # to that resource table
                    foreign_table_name = link.split("vocab:")[1]
                    attr_dict[title] = Column(
                        String,
                        ForeignKey(
                            f"{foreign_table_name}.id",
                            ondelete="CASCADE",
                            onupdate="CASCADE",
                        ),
                    )
                else:
                    attr_dict[title] = Column(String)
            else:
                foreign_table_name = link["range"].split("vocab:")[1]
                attr_dict[title] = Column(
                    String,
                    ForeignKey(
                        f"{foreign_table_name}.id",
                        ondelete="CASCADE",
                        onupdate="CASCADE",
                    ),
                )
        return attr_dict

    def make_db_table(self):
        self.table_class = type(self.name, (Base,), self.get_attr_dict())
        Resource.all_database_classes[self.name] = self.table_class


# single_class = classes[6]
# resource = Resource(single_class)
# a = resource.get_attr_dict()


def get_type(object_):
    return object_["@type"]


def insert_object(object_):
    type_ = get_type(object_)
    database_class = get_database_class(type_)
    object_.pop("@type")
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
        contraint_error = e.orig
        raise DatabaseConstraintError(contraint_error)
    return inserted_object.id


def get_database_class(type_):
    database_class = Resource.all_database_classes.get(type_, None)
    if database_class is None:
        raise ClassNotFound(type_)
    return database_class


def get_object(query_info):
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
    object_.pop("_sa_instance_state")
    object_.pop("id")
    object_["@type"] = query_info["@type"]
    return object_


def delete_object(query_info):
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
    session.commit()


def update_object(object_, query_info):
    """Update the object from the database"""
    # Keep the object as fail safe
    old_object = get_object(query_info)
    # Delete the old object
    delete_object(query_info)
    id_ = query_info["id_"]
    # Try inserting new object
    try:
        object_["id"] = id_
        d = insert_object(object_)
    except Exception as e:
        # Put old object back
        old_object["id"] = id_
        d = insert_object(old_object)
        raise e
    return id_


for single_class in classes:
    resource = Resource(single_class)
    resource.make_db_table()

# print("Creating models....")
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
# print("Done")

# object_ = {
#     "@type": "State",
#     "Speed": "100",
#     "Position": "101",
#     "Direction": "102",
#     "Battery": "103",
#     "SensorStatus": "104",
#     "DroneID": "105",
# }

# object_ = {
#     "@type": "Command",
#     "State": "3e1d8fb4-df1a-41b6-a9b4-ded0f94dc196",
#     "DroneID": "5",
# }
# d = insert_object(object_)
query_info = {
    "@type": "Command",
    "id_": "16e7b9de-241f-432b-9b59-ac12a4279ce0",
}
d = get_object(query_info)
print(d)
# delete_object(query_info)
# object_ = {
#     "@type": "Command",
#     "State": "3e1d8fb4-df1a-41b6-a9b4-ded0f94dc196",
#     "DroneID": "18",
# }
# d = update_object(object_, query_info)

# print(d)
