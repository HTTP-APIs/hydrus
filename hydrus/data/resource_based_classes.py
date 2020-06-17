"""
Script to generate the tables in hydrus database based on
resources in the provided API Doc.
"""
import uuid

from hydra_python_core import doc_maker
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from hydrus.conf import APIDOC_OBJ
from hydrus.data.doc_parse import get_classes
from hydrus.data.exceptions import ClassNotFound

serverurl = "http://localhost"
port = 8080
HYDRUS_SERVER_URL = f"{serverurl}:{str(port)}/"
API_NAME = "serverapi"
apidoc = doc_maker.create_doc(APIDOC_OBJ, HYDRUS_SERVER_URL, API_NAME)

classes = get_classes(apidoc.generate())
class_names = []

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
            attr_dict[title] = Column(String)
        return attr_dict

    def make_db_table(self):
        self.table_class = type(self.name, (Base,), self.get_attr_dict())
        Resource.all_database_classes[self.name] = self.table_class


all_database_classes = {}
single_class = classes[2]
resource = Resource(single_class)
resource.make_db_table()
# print(Resource.all_database_classes)


class Object:
    def __init__(self, object_):
        self.object_ = object_
        self.type_ = self.get_type()
        self.database_class = get_database_class(self.type_)

    def get_type(self):
        return self.object_["@type"]

    def insert(self):
        self.object_.pop("@type")
        try:
            inserted_object = self.database_class(**self.object_)
        except TypeError as e:
            # TODO: Raise PropertyNotFound exception
            return print(e.args)
        session.add(inserted_object)
        session.commit()
        return inserted_object.id


def get_database_class(type_):
    database_class = Resource.all_database_classes.get(type_, None)
    if database_class is None:
        raise ClassNotFound(type_)
    return database_class


def get_object_from_db(query_info):
    database_class = get_database_class(query_info["@type"])
    id_ = query_info["id_"]
    object_ = (
        session.query(database_class).filter(database_class.id == id_).one()
    ).__dict__
    object_.pop("_sa_instance_state")
    object_.pop("id")
    object_["@type"] = query_info["@type"]
    return object_


def delete_object_from_db(query_info):
    database_class = get_database_class(query_info["@type"])
    id_ = query_info["id_"]
    object_ = (
        session.query(database_class).filter(database_class.id == id_).one()
    )
    session.delete(object_)
    session.commit()


def update_object_from_db(object_, query_info):
    # Keep the object as fail safe
    old_object = get_object_from_db(query_info)
    # Delete the old object
    delete_object_from_db(query_info)
    id_ = query_info["id_"]
    # Try inserting new object
    try:
        object_["id"] = id_
        data = Object(object_)
        d = data.insert()
    except (TypeError) as e:
        # Put old object back
        old_object["id"] = id_
        data = Object(old_object)
        d = data.insert()
        raise e
    return id_


# for single_class in classes:
#     resource = Resource(single_class)
#     resource.make_db_table()

# print("Creating models....")
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
# print("Done")

object_ = {
    "@type": "Message",
    "MessageString": "a gggg Good Message",
}
# data = Object(object_)
# d = data.insert()
query_info = {
    "@type": "Message",
    "id_": "007a98aa-2009-4a6b-9bc1-15bfa31027ae",
}

# d = get_object_from_db(query_info)
# delete_object_from_db(query_info)
d = update_object_from_db(object_, query_info)

print(d)
