"""Unit tests for CRUD operations in hydrus.data.crud."""

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hydrus.data.crud as crud
from hydrus.data.db_models import Base
from hydrus.hydraspec.vocab_generator import gen_vocab
from hydrus.data.insert_classes import gen_classes

def object_1():
    """Return a copy of an object."""
    object_ = {
        "name": "helllo",
        "@type": "Spacecraft_Communication",
        "status": {
            "name": "xa",
            "@type": "status",
            "Identifier": -1000,
            "Speed": 0,
            "Position": "0,0",
            "Battery": 100,
            "Destination": "0,0",
            "Sensor": "temprature",
            "Status": "Started"
        }
    }
    return object_


def object_2():
    """Return a copy of another object."""
    object_ = {
        "name": "helllo2",
        "@type": "Spacecraft_Communication",
        "status": {
            "name": "xadjal",
            "@type": "status",
            "Identifier": -1000,
            "Speed": 0,
            "Position": "0,1",
            "Battery": 100,
            "Destination": "1,0",
            "Sensor": "temprature",
            "Status": "Stopped"
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
        test_labels = ["Spacecraft_Communication", "status"]
        test_classes = gen_classes(test_labels)

        self.session.add_all(test_classes)
        self.session.commit()
        print("Test Classes added successfully.")

        print("Setup done, running tests...")

    def test_insert(self):
        """Test CRUD insert."""
        object_ = object_1()
        response = crud.insert(object_=object_, id_=1, session=self.session)
        assert 201 in response

    def test_get(self):
        """Test CRUD get."""
        object_ = object_1()
        id_ = 2
        response = crud.insert(object_=object_, id_=id_, session=self.session)
        object_ = crud.get(id_=id_, type_=object_["@type"], session=self.session)
        assert 201 in response
        assert int(object_["@id"].split("/")[-1]) == id_

    def test_update(self):
        """Test CRUD update."""
        object_ = object_1()
        new_object = object_2()
        id_ = 30
        insert_response = crud.insert(object_=object_, id_=id_, session=self.session)
        update_response = crud.update(id_=id_, type_=object_["@type"], object_=new_object, session=self.session)
        test_object = crud.get(id_=id_, type_=object_["@type"], session=self.session)
        assert 201 in insert_response
        assert 200 in update_response
        assert int(test_object["@id"].split("/")[-1]) == id_

    def test_delete(self):
        """Test CRUD delete."""
        object_ = object_1()
        id_ = 4
        insert_response = crud.insert(object_=object_, id_=id_, session=self.session)
        delete_response = crud.delete(id_=id_, type_=object_["@type"], session=self.session)
        get_response = crud.get(id_=id_, type_=object_["@type"], session=self.session)
        assert 201 in insert_response
        assert 200 in delete_response
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
        assert 400 in get_response

    def test_delete_type(self):
        """Test CRUD delete when wrong/undefined class is given."""
        object_ = object_1()
        id_ = 50
        insert_response = crud.insert(object_=object_, id_=id_, session=self.session)
        delete_response = crud.delete(id_=id_, type_="dummyClass", session=self.session)
        assert 201 in insert_response
        assert 400 in delete_response

    def test_delete_id(self):
        """Test CRUD delete when wrong/undefined ID is given."""
        object_ = object_1()
        id_ = 6
        insert_response = crud.insert(object_=object_, id_=id_, session=self.session)
        delete_response = crud.delete(id_=999, type_=object_["@type"], session=self.session)
        assert 201 in insert_response
        assert 404 in delete_response

    def test_insert_type(self):
        """Test CRUD insert when wrong/undefined class is given."""
        object_ = object_1()
        id_ = 7
        object_["@type"] = "dummyClass"
        insert_response = crud.insert(object_=object_, id_=id_, session=self.session)
        assert 400 in insert_response

    def test_insert_id(self):
        """Test CRUD insert when used ID is given."""
        object_ = object_1()
        id_ = 1
        insert_response = crud.insert(object_=object_, id_=id_, session=self.session)
        assert 400 in insert_response


    def test_insert_abstractproperty(self):
        """Test CRUD when AbstractProperty is given instance."""
        object_ = object_1()
        id_ = 9
        object_["dummyAbstractProperty"] = "Spacecraft_Communication"
        insert_response_1 = crud.insert(object_=object_, id_=id_, session=self.session)
        object_["dummyAbstractProperty"] = 4
        insert_response_2 = crud.insert(object_=object_, id_=id_+1, session=self.session)
        assert 201 in insert_response_1
        assert 400 in insert_response_2

    def test_insert_instanceproperty(self):
        """Test CRUD when InstanceProperty is given Class."""
        object_ = object_1()
        id_ = 10
        insert_response_1 = crud.insert(object_=object_, id_=id_, session=self.session)
        object_["hasMass"] = "Spacecraft_Communication"
        insert_response_2 = crud.insert(object_=object_, id_=id_+1, session=self.session)
        print(insert_response_1,insert_response_2)
        assert 201 in insert_response_1
        assert 201 in insert_response_2

    @classmethod
    def tearDownClass(self):
        """Undo the setUp steps for the Class."""
        self.session.close()


if __name__ == '__main__':
    unittest.main()
