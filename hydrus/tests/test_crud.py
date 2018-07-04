"""Unit tests for CRUD operations in hydrus.data.crud."""

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import hydrus.data.crud as crud
from hydrus.data.db_models import Base
from hydrus.data import doc_parse
from hydrus.samples.doc_writer_sample import api_doc as doc
import random
import string


def gen_dummy_object(class_, doc):
    """Create a dummy object based on the definitions in the API Doc."""
    object_ = {
        "@type": class_
    }
    if class_ in doc.parsed_classes:
        for prop in doc.parsed_classes[class_]["class"].supportedProperty:
            if "vocab:" in prop.prop:
                prop_class = prop.prop.replace("vocab:", "")
                object_[prop.title] = gen_dummy_object(prop_class, doc)
            else:
                object_[prop.title] = ''.join(random.choice(
                    string.ascii_uppercase + string.digits) for _ in range(6))
        return object_


class TestCRUD(unittest.TestCase):
    """Test class for CRUD Tests."""

    @classmethod
    def setUpClass(self):
        """Database setup before the CRUD tests."""
        print("Creating a temporary datatbsse...")
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        session = scoped_session(sessionmaker(bind=engine))

        self.session = session
        self.doc = doc
        test_classes = doc_parse.get_classes(self.doc.generate())
        test_properties = doc_parse.get_all_properties(test_classes)
        doc_parse.insert_classes(test_classes, self.session)
        doc_parse.insert_properties(test_properties, self.session)
        print("Classes and properties added successfully.")
        print("Setup done, running tests...")

    def test_insert(self):
        """Test CRUD insert."""
        object_ = gen_dummy_object("dummyClass", self.doc)
        response = crud.insert(object_=object_, id_=1, session=self.session)
        assert type(response) is int

    def test_get(self):
        """Test CRUD get."""
        object_ = gen_dummy_object("dummyClass", self.doc)
        id_ = 2
        response = crud.insert(object_=object_, id_=id_, session=self.session)
        object_ = crud.get(id_=id_, type_=object_[
                           "@type"], session=self.session, api_name="api")
        assert type(response) is int
        assert int(object_["@id"].split("/")[-1]) == id_

    def test_update(self):
        """Test CRUD update."""
        object_ = gen_dummy_object("dummyClass", self.doc)
        new_object = gen_dummy_object("dummyClass", self.doc)
        id_ = 30
        insert_response = crud.insert(
            object_=object_, id_=id_, session=self.session)
        update_response = crud.update(id_=id_, type_=object_[
                                      "@type"], object_=new_object, session=self.session, api_name="api")
        test_object = crud.get(id_=id_, type_=object_[
                               "@type"], session=self.session, api_name="api")
        assert type(insert_response) is int
        assert type(update_response) is int
        assert insert_response == update_response
        assert int(test_object["@id"].split("/")[-1]) == id_

    def test_delete(self):
        """Test CRUD delete."""
        object_ = gen_dummy_object("dummyClass", self.doc)
        id_ = 4
        insert_response = crud.insert(
            object_=object_, id_=id_, session=self.session)
        delete_response = crud.delete(
            id_=id_, type_=object_["@type"], session=self.session)
        assert type(insert_response) is int
        response_code = None
        try:
            get_response = crud.get(id_=id_, type_=object_[
                                    "@type"], session=self.session, api_name="api")
        except Exception as e:
            response_code, message = e.get_HTTP()
        assert 404 == response_code

    def test_get_id(self):
        """Test CRUD get when wrong/undefined ID is given."""
        id_ = 999
        type_ = "dummyClass"
        response_code = None
        try:
            get_response = crud.get(
                id_=id_, type_=type_, session=self.session, api_name="api")
        except Exception as e:
            response_code, message = e.get_HTTP()
        assert 404 == response_code

    def test_get_type(self):
        """Test CRUD get when wrong/undefined class is given."""
        id_ = 1
        type_ = "otherClass"
        response_code = None
        try:
            get_response = crud.get(
                id_=id_, type_=type_, session=self.session, api_name="api")
        except Exception as e:
            response_code, message = e.get_HTTP()
        assert 400 == response_code

    def test_delete_type(self):
        """Test CRUD delete when wrong/undefined class is given."""
        object_ = gen_dummy_object("dummyClass", self.doc)
        id_ = 50
        insert_response = crud.insert(
            object_=object_, id_=id_, session=self.session)
        assert type(insert_response) is int
        assert insert_response == id_
        response_code = None
        try:
            delete_response = crud.delete(
                id_=id_, type_="otherClass", session=self.session)
        except Exception as e:
            response_code, message = e.get_HTTP()
        assert 400 == response_code

    def test_delete_id(self):
        """Test CRUD delete when wrong/undefined ID is given."""
        object_ = gen_dummy_object("dummyClass", self.doc)
        id_ = 6
        insert_response = crud.insert(
            object_=object_, id_=id_, session=self.session)
        response_code = None
        try:
            delete_response = crud.delete(
                id_=999, type_=object_["@type"], session=self.session)
        except Exception as e:
            response_code, message = e.get_HTTP()
        assert 404 == response_code
        assert type(insert_response) is int
        assert insert_response == id_

    def test_insert_type(self):
        """Test CRUD insert when wrong/undefined class is given."""
        object_ = gen_dummy_object("dummyClass", self.doc)
        id_ = 7
        object_["@type"] = "otherClass"
        response_code = None
        try:
            insert_response = crud.insert(
                object_=object_, id_=id_, session=self.session)
        except Exception as e:
            response_code, message = e.get_HTTP()
        assert 400 == response_code

    def test_insert_id(self):
        """Test CRUD insert when used ID is given."""
        object_ = gen_dummy_object("dummyClass", self.doc)
        id_ = 1
        response_code = None
        try:
            insert_response = crud.insert(
                object_=object_, id_=id_, session=self.session)
        except Exception as e:
            response_code, message = e.get_HTTP()
        assert 400 == response_code

    def test_insert_ids(self):
        """Test CRUD insert when multiple ID's are given """
        object = gen_dummy_object("dummyClass",self.doc)
        ids = "1,2,3"
        response_code = None
        try:
            

    @classmethod
    def tearDownClass(self):
        """Undo the setUp steps for the Class."""
        self.session.close()


if __name__ == '__main__':
    unittest.main()
