"""Models for Hydra Classes."""

import datetime
import uuid
from sqlite3 import Connection as SQLite3Connection
from typing import Any

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
    event,
)
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# from hydrus.settings import DB_URL

engine = create_engine("sqlite:///database.db")

Base = declarative_base()  # type: Any

EXPIRY_TIME = 2700  # unit: seconds


# required for enforcing foreign key constraints through SQLite
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


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


class Modification(Base):
    """Model for sync related state-changing modifications."""

    __tablename__ = "modifications"

    job_id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(String)
    resource_url = Column(String)


class User(Base):
    """Model for a user that stores the ID, paraphrase and a nonce."""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    paraphrase = Column(String)


class Token(Base):
    """Model for storing tokens for the users."""

    __tablename__ = "tokens"
    id = Column(
        String,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        primary_key=True,
    )
    user_id = Column(Integer, ForeignKey("user.id"))
    timestamp = Column(DateTime, default=func.now())
    expiry = Column(
        "expiry",
        DateTime,
        default=datetime.datetime.utcnow()
        + datetime.timedelta(seconds=EXPIRY_TIME),
    )

    def is_valid(self):
        if self.expiry > datetime.datetime.utcnow():
            return True
        return False


class Nonce(Base):
    """Model for storing nonce for the users."""

    __tablename__ = "nonce"
    id = Column(String, primary_key=True)
    timestamp = Column(DateTime)


def create_database_tables(classes):
    for single_class in classes:
        resource = Resource(single_class)
        resource.make_db_table()


if __name__ == "__main__":
    print("Creating models....")
    Base.metadata.create_all(engine)
    print("Done")
