import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hydrus.data.crud import get, insert, delete, update
from hydrus.data.db_models import engine

import pdb

object_1 = {
    "name": "12W communiscation",
    "object": {
        "category": "Spacecraft_Communication",
        "hasMass": 9000,
        "hasMonetaryValue": 4,
        "hasPower": -61,
        "hasVolume": 99,
        "maxWorkingTemperature": 63,
        "minWorkingTemperature": -26
    }
}

object_2 = {
    "name": "150W communication",
    "object": {
        "category": "Spacecraft_Communication",
        "hasMass": 00,
        "hasMonetaryValue": 40,
        "hasPower": -61,
        "hasVolume": 95,
        "maxWorkingTemperature": 60,
        "minWorkingTemperature": -20
    }
}


class TestQuery(unittest.TestCase):

    def setup(self):
        Session = sessionmaker(bind=engine)
        session = Session()

    def test_insert(self):
        """Test insertion from crud."""
        object_ = object_1
        insert_id = 1002
        insert_id = insert(object_=object_, id_=1002)
        assert type(insert_id) != dict
        assert int(insert_id) > 0

    def test_get(self):
        """Test get from crud."""
        insert_id = 3
        object_ = get(id_=insert_id)
        assert object_ != {404: "Instance with ID : %s NOT FOUND" % insert_id}
        assert int(object_["@id"]) == insert_id

    def test_update(self):
        """Test update from crud."""
        object_ = object_2
        insert_id = 8
        update_response = update(id_=insert_id, object_=object_)

        assert 204 in update_response.keys()

    def test_delete(self):
        """Test deletion from crud."""
        insert_id = 1007

        del_ = delete(id_=insert_id)
        assert get(insert_id) == {
            404: "Instance with ID : %s NOT FOUND" % insert_id}

    def teardown(self):
        session.remove()


if __name__ == '__main__':
    unittest.main()
