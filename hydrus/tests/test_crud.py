"""Unit tests for CRUD operations in hydrus.data.crud."""

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hydrus.data.crud as crud
from hydrus.data.db_models import Base
from hydrus.hydraspec.vocab_generator import gen_vocab
import hydrus.data.doc_parse as parser
from hydrus.app import SERVER_URL, SEMANTIC_REF_URL, SEMANTIC_REF_NAME, PARSED_CLASSES

def object_1():
    """Return a copy of an object."""
    object_ = {
        "name": "12W communication",
        "@type": "Spacecraft_Communication",
        "object": {
            "hasMass": 9000,
            "hasMonetaryValue": 4,
            "hasPower": -61,
            "hasVolume": 99,
            "maxWorkingTemperature": 63,
            "minWorkingTemperature": -26
        }
    }
    return object_


def object_2():
    """Return a copy of another object."""
    object_ = {
        "name": "150W communication",
        "@type": "Spacecraft_Communication",
        "object": {
            "hasMass": 00,
            "hasMonetaryValue": 40,
            "hasPower": -61,
            "hasVolume": 95,
            "maxWorkingTemperature": 60,
            "minWorkingTemperature": -20
        }
    }
    return object_


class TestCRUD(unittest.TestCase):
    """Test class for CRUD Tests."""

    @classmethod
    def setUpClass(self):
        """Database setup before the CRUD tests."""
        print("Creating a temporary datatbsse...")
        engine = create_engine('sqlite:///:memory:')
        self.engine = engine

        print("Creating models...")
        Base.metadata.create_all(engine)

        print("Starting session...")
        Session = sessionmaker(bind=engine)
        session = Session()
        self.session = session

        print("Adding Classes...")
        classes = parser.get_classes(gen_vocab(PARSED_CLASSES, SERVER_URL, SEMANTIC_REF_NAME, SEMANTIC_REF_URL))
        parser.insert_classes(classes, self.session)

        print("Adding Properties...")
        properties = parser.get_all_properties(classes)
        parser.insert_properties(properties, self.session)

        print("Setup done, running tests...")

    def test_insert(self):
        """Test CRUD insert."""
        object_ = object_1()
        response = crud.insert(object_=object_, id_=1, session=self.session)
        assert 204 in response

    def test_get(self):
        """Test CRUD get."""
        object_ = object_1()
        id_ = 2
        response = crud.insert(object_=object_, id_=id_, session=self.session)
        object_ = crud.get(id_=id_, type_=object_["@type"], session=self.session)
        assert 204 in response
        assert "object" in object_
        assert int(object_["@id"].split("/")[-1]) == id_

    def test_update(self):
        """Test CRUD update."""
        object_ = object_1()
        new_object = object_2()
        id_ = 3
        insert_response = crud.insert(object_=object_, id_=id_, session=self.session)
        update_response = crud.update(id_=id_, type_=object_["@type"], object_=new_object, session=self.session)
        test_object = crud.get(id_=id_, type_=object_["@type"], session=self.session)
        assert 204 in insert_response
        assert 204 in update_response
        assert int(test_object["@id"].split("/")[-1]) == id_

    def test_delete(self):
        """Test CRUD delete."""
        object_ = object_1()
        id_ = 4
        insert_response = crud.insert(object_=object_, id_=id_, session=self.session)
        delete_response = crud.delete(id_=id_, type_=object_["@type"], session=self.session)
        get_response = crud.get(id_=id_, type_=object_["@type"], session=self.session)
        assert 204 in insert_response
        assert 204 in delete_response
        assert 404 in get_response

    def test_get_id(self):
        """Test CRUD get when wrong/undefined ID is given."""
        id_ = 999
        type_ = "Spacecraft_Communication"
        get_response = crud.get(id_=id_, type_=type_, session=self.session)
        assert 404 in get_response

    def test_get_type(self):
        """Test CRUD get when wrong/undefined class is given."""
        id_ = 1
        type_ = "dummyClass"
        get_response = crud.get(id_=id_, type_=type_, session=self.session)
        assert 401 in get_response

    def test_delete_type(self):
        """Test CRUD delete when wrong/undefined class is given."""
        object_ = object_1()
        id_ = 5
        insert_response = crud.insert(object_=object_, id_=id_, session=self.session)
        delete_response = crud.delete(id_=id_, type_="dummyClass", session=self.session)
        assert 204 in insert_response
        assert 401 in delete_response

    def test_delete_id(self):
        """Test CRUD delete when wrong/undefined ID is given."""
        object_ = object_1()
        id_ = 6
        insert_response = crud.insert(object_=object_, id_=id_, session=self.session)
        delete_response = crud.delete(id_=999, type_=object_["@type"], session=self.session)
        assert 204 in insert_response
        assert 404 in delete_response

    def test_insert_type(self):
        """Test CRUD insert when wrong/undefined class is given."""
        object_ = object_1()
        id_ = 7
        object_["@type"] = "dummyClass"
        insert_response = crud.insert(object_=object_, id_=id_, session=self.session)
        assert 401 in insert_response

    def test_insert_id(self):
        """Test CRUD insert when used ID is given."""
        object_ = object_1()
        id_ = 1
        insert_response = crud.insert(object_=object_, id_=id_, session=self.session)
        assert 400 in insert_response

    def test_insert_instance(self):
        """Test CRUD insert when used invalid instance is given."""
        object_ = object_1()
        id_ = 8
        object_["object"]["hasDuplicate"] = {"@id": 999}
        insert_response_1 = crud.insert(object_=object_, id_=id_, session=self.session)
        object_["object"]["hasDuplicate"] = {"id": 999}
        insert_response_2 = crud.insert(object_=object_, id_=id_, session=self.session)
        assert 403 in insert_response_1
        assert 403 in insert_response_2

    def test_insert_abstractproperty(self):
        """Test CRUD when AbstractProperty is given instance."""
        object_ = object_1()
        id_ = 9
        object_["object"]["dummyAbstractProperty"] = "Spacecraft_Communication"
        insert_response_1 = crud.insert(object_=object_, id_=id_, session=self.session)
        object_["object"]["dummyAbstractProperty"] = 4
        insert_response_2 = crud.insert(object_=object_, id_=id_+1, session=self.session)
        assert 204 in insert_response_1
        assert 402 in insert_response_2

    def test_insert_instanceproperty(self):
        """Test CRUD when InstanceProperty is given Class."""
        object_ = object_1()
        id_ = 10
        insert_response_1 = crud.insert(object_=object_, id_=id_, session=self.session)
        object_["object"]["hasMass"] = "Spacecraft_Communication"
        insert_response_2 = crud.insert(object_=object_, id_=id_+1, session=self.session)
        assert 204 in insert_response_1
        assert 402 in insert_response_2

    @classmethod
    def tearDownClass(self):
        """Undo the setUp steps for the Class."""
        self.session.close()


if __name__ == '__main__':
    unittest.main()
