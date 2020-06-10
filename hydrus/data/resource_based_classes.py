"""
Script to generate the tables in hydrus database based on
resources in the provided API Doc.
"""
import uuid

from hydra_python_core import doc_maker
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

from hydrus.conf import APIDOC_OBJ
from hydrus.data.doc_parse import get_classes

serverurl = "http://localhost"
port = 8080
HYDRUS_SERVER_URL = f"{serverurl}:{str(port)}/"
API_NAME = "serverapi"
apidoc = doc_maker.create_doc(APIDOC_OBJ, HYDRUS_SERVER_URL, API_NAME)

classes = get_classes(apidoc.generate())
class_names = []

engine = create_engine("sqlite:///database2.db")
Base = declarative_base()


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


for single_class in classes:
    resource = Resource(single_class)
    resource.make_db_table()

print("Creating models....")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
print("Done")
