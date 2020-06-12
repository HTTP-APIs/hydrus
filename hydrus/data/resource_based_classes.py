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

serverurl = "http://localhost"
port = 8080
HYDRUS_SERVER_URL = f"{serverurl}:{str(port)}/"
API_NAME = "serverapi"
apidoc = doc_maker.create_doc(APIDOC_OBJ, HYDRUS_SERVER_URL, API_NAME)

classes = get_classes(apidoc.generate())
class_names = []

engine = create_engine("sqlite:///database1.db")
Base = declarative_base()
# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()


class Resource:
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


all_database_classes = {}
single_class = classes[2]
resource = Resource(single_class)
resource.make_db_table()
all_database_classes[resource.name] = resource.table_class
print(all_database_classes)


class Object:
    def __init__(self, object_):
        self.object_ = object_
        self.type_ = self.get_type()
        self.database_class = self.get_database_class()

    def get_type(self):
        return self.object_["@type"]

    def insert_object(self):
        self.object_.pop("@type")
        inserted_object = self.database_class(**self.object_)
        session.add(inserted_object)
        session.commit()
        return inserted_object

    def get_database_class(self):
        return all_database_classes[self.type_]


# for single_class in classes:
#     resource = Resource(single_class)
#     resource.make_db_table()

# print("Creating models....")
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
# print("Done")

object_ = {
    "@type": "Message",
    "MessageString": "VV Good Message",
}
data = Object(object_)
d = data.insert_object()
print(d)
