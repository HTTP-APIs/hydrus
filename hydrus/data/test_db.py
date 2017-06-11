import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crud import get, insert, delete, update
from generator import gen_random_object

import pdb

from db_models import Base


class TestQuery(unittest.TestCase):

    engine = create_engine('sqlite:///test_database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    def setup(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)

    def test_insert(self):
        """Test insertion from crud."""
        object_ = gen_random_object()
        inserted_obj_id = insert(object_)
        assert type(inserted_obj_id) != dict
        assert int(inserted_obj_id) > 0

    def test_get(self):
        """Test get from crud."""
        id_ = 1
        object_ = get(id_)

        assert object_ != {404: "Instance with ID : %s NOT FOUND" % id_}
        assert int(object_["@id"]) > 0

    def test_update(self):
        """Test update from crud."""
        object_ = gen_random_object()
        id_ = 1

        update(id_, object_)
        assert get(id_) == object_

    def test_delete(self):
        """Test deletion from crud."""
        id_ = 1

        del_ = delete(id_)
        assert del_.has_key(204)
        assert get(id_) == {404: "Instance with ID : %s NOT FOUND" % id_}

    def teardown(self):
        session.remove()


if __name__ == '__main__':
    unittest.main()
