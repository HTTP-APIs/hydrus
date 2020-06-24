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
    InstanceNotFound,
    PropertyNotFound,
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

# required for enforcing foreign key constraints through SQLite
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
    """
    Class for interacting with any resource(class or collection) in the ApiDoc
    """

    # TODO: Look for a better way to store the sql alchemy class for each resource
    all_database_classes = {}

    def __init__(self, resource):
        self._resource = resource

    @property
    def name(self):
        """Return the name of the resource from it's "@id"""
        # split the classname at "vocab:" to get the class name
        return self._resource["@id"].split("vocab:")[1]

    @property
    def resource(self):
        """Return the resource dict"""
        return self._resource

    @property
    def supported_properties(self):
        """
        Return all the properties in "supportedProperty" property
        of that resource.
        """
        return self._resource["supportedProperty"]

    def get_attr_dict(self):
        """
        Return the attribute dictionary necessary for
        creating that resource's table at runtime
        """
        # initialize the attribute dict with "__tablename__"
        # and a "id" column which will act as primary key
        # for instances of that table
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
                    attr_dict[title] = Resource.foreign_key_column(
                        foreign_table_name
                    )

                else:
                    attr_dict[title] = Column(String)
            else:
                # if the supported property has "property" attribute of @type "hydra:link"
                if "vocab:" in link["range"]:
                    # if vocab: is in the link["range"], it implies that the link is pointing to
                    # another resource in the same ApiDoc, hence make it a Foreign Key
                    # to that resource table
                    foreign_table_name = link["range"].split("vocab:")[1]
                    attr_dict[title] = Resource.foreign_key_column(
                        foreign_table_name
                    )
                else:
                    attr_dict[title] = Column(String)

        return attr_dict

    @staticmethod
    def foreign_key_column(foreign_table_name):
        """
        Return a sqlalchemy column which will act as
        a foreign key to given tablename.
        """

        return Column(
            String,
            ForeignKey(
                f"{foreign_table_name}.id",
                ondelete="CASCADE",
                onupdate="CASCADE",
            ),
        )

    def make_db_table(self):
        """Generate the sqlalchemy table class for that resource"""
        self.table_class = type(self.name, (Base,), self.get_attr_dict())
        # add that class to dict for future lookups
        Resource.all_database_classes[self.name] = self.table_class


def get_type(object_):
    """Return the @type of that given object"""
    return object_["@type"]


def get_database_class(type_):
    """Get the sqlalchemy class object from given classname"""
    database_class = Resource.all_database_classes.get(type_, None)
    if database_class is None:
        raise ClassNotFound(type_)
    return database_class


def insert_object(object_):
    """Insert the object in the database"""
    type_ = get_type(object_)
    database_class = get_database_class(type_)
    # remove the @type from object before using the object to make a
    # instance of it using sqlalchemy class
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


def get_object(query_info):
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

print("Creating models....")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
print("Done")
