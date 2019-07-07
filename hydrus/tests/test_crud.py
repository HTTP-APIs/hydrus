"""Unit tests for CRUD operations in hydrus.data.crud."""

import unittest
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import hydrus.data.crud as crud
from hydrus.data.db_models import Base
from hydrus.data import doc_parse
from hydra_python_core import doc_maker
from hydrus.samples.hydra_doc_sample import doc

import random
from typing import List
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
        self.API_NAME = "demoapi"
        self.HYDRUS_SERVER_URL = "http://hydrus.com/"
        self.session = session

        self.doc = doc_maker.create_doc(
            doc, self.HYDRUS_SERVER_URL, self.API_NAME)

        test_classes = doc_parse.get_classes(self.doc.generate())

        # Getting list of classes from APIDoc
        self.doc_collection_classes = [
            self.doc.collections[i]["collection"].class_.title for i in self.doc.collections]
        print(self.doc_collection_classes)
        print(random.choice(self.doc_collection_classes))
        test_properties = doc_parse.get_all_properties(test_classes)
        doc_parse.insert_classes(test_classes, self.session)
        doc_parse.insert_properties(test_properties, self.session)
        print("Classes and properties added successfully.")
        print("Setup done, running tests...")

    def test_insert(self):
        """Test CRUD insert."""
        object_ = gen_dummy_object(random.choice(
            self.doc_collection_classes), self.doc)
        id_ = str(uuid.uuid4())
        response = crud.insert(object_=object_, id_=id_, session=self.session)

        assert isinstance(response, str)

    def test_get(self):
        """Test CRUD get."""
        object_ = gen_dummy_object(random.choice(
            self.doc_collection_classes), self.doc)
        id_ = str(uuid.uuid4())
        response = crud.insert(object_=object_, id_=id_, session=self.session)
        object_ = crud.get(id_=id_, type_=object_[
                           "@type"], session=self.session, api_name="api")
        assert isinstance(response, str)
        assert object_["@id"].split("/")[-1] == id_

    def test_get_for_nested_obj(self):
        """Test get operation for object that can contain other objects."""
        for class_ in self.doc_collection_classes:
            for prop in self.doc.parsed_classes[class_]["class"].supportedProperty:
                if "vocab:" in prop.prop:
                    nested_class = prop.prop.replace("vocab:", "")
                    object_ = gen_dummy_object(class_, self.doc)
                    obj_id = str(uuid.uuid4())
                    response = crud.insert(object_=object_, id_=obj_id, session=self.session)
                    object_ = crud.get(id_=obj_id, type_=class_, session=self.session,
                                       api_name="api")
                    assert prop.title in object_
                    nested_obj_id = object_[prop.title]
                    nested_obj = crud.get(id_=nested_obj_id, type_=nested_class,
                                          session=self.session, api_name="api")
                    assert nested_obj["@id"].split("/")[-1] == nested_obj_id
                    break

    def test_searching(self):
        """Test searching over collection elements."""
        for class_ in self.doc_collection_classes:
            target_property_1 = ""
            target_property_2 = ""
            for prop in self.doc.parsed_classes[class_]["class"].supportedProperty:
                # Find nested object so we can test searching of elements by properties of nested objects.
                if "vocab:" in prop.prop:
                    object_ = gen_dummy_object(class_, self.doc)
                    # Setting property of a nested object as target
                    for property_ in object_[prop.title]:
                        if property_ != "@type":
                            object_[prop.title][property_] = "target_1"
                            target_property_1 = "{}[{}]".format(prop.title, property_)
                            break
                    break
                elif target_property_1 is not "":
                    for property_ in object_:
                        if property_ != "@type":
                            object_[property_] = "target_2"
                            target_property_2 = property_
                            break
                    break

                if target_property_1 is not "" and target_property_2 is not "":
                    # Set search parameters
                    search_params = {
                        target_property_1: "target_1",
                        target_property_2: "target_2"
                    }

                    obj_id = str(uuid.uuid4())
                    response = crud.insert(object_=object_, id_=obj_id, session=self.session)
                    search_result = crud.get_collection(API_NAME="api", type_=class_, session=self.session,
                                                        paginate=True, page_size=5, search_params=search_params)
                    assert len(search_result["members"]) > 0
                    search_item_id = search_result["members"][0]["@id"].split('/')[-1]
                    assert search_item_id == obj_id
                    break

    def test_update(self):
        """Test CRUD update."""
        random_class = random.choice(self.doc_collection_classes)
        object_ = gen_dummy_object(random_class, self.doc)
        new_object = gen_dummy_object(random_class, self.doc)
        id_ = str(uuid.uuid4())
        insert_response = crud.insert(
            object_=object_, id_=id_, session=self.session)
        update_response = crud.update(
            id_=id_,
            type_=object_["@type"],
            object_=new_object,
            session=self.session,
            api_name="api")
        test_object = crud.get(id_=id_, type_=object_[
                               "@type"], session=self.session, api_name="api")
        assert isinstance(insert_response, str)
        assert isinstance(update_response, str)
        assert insert_response == update_response
        assert test_object["@id"].split("/")[-1] == id_

    def test_delete(self):
        """Test CRUD delete."""
        object_ = gen_dummy_object(random.choice(
            self.doc_collection_classes), self.doc)
        id_ = str(uuid.uuid4())
        insert_response = crud.insert(
            object_=object_, id_=id_, session=self.session)
        delete_response = crud.delete(
            id_=id_, type_=object_["@type"], session=self.session)
        assert isinstance(insert_response, str)
        response_code = None
        try:
            get_response = crud.get(
                id_=id_,
                type_=object_["@type"],
                session=self.session,
                api_name="api")
        except Exception as e:
            error = e.get_HTTP()
        assert 404 == error.code

    def test_get_id(self):
        """Test CRUD get when wrong/undefined ID is given."""
        id_ = str(uuid.uuid4())
        type_ = random.choice(self.doc_collection_classes)
        response_code = None
        try:
            get_response = crud.get(
                id_=id_, type_=type_, session=self.session, api_name="api")
        except Exception as e:
            error = e.get_HTTP()
        assert 404 == error.code

    def test_get_type(self):
        """Test CRUD get when wrong/undefined class is given."""
        id_ = str(uuid.uuid4())
        type_ = "otherClass"
        response_code = None
        try:
            get_response = crud.get(
                id_=id_, type_=type_, session=self.session, api_name="api")
        except Exception as e:
            error = e.get_HTTP()
        assert 400 == error.code

    def test_delete_type(self):
        """Test CRUD delete when wrong/undefined class is given."""
        object_ = gen_dummy_object(random.choice(
            self.doc_collection_classes), self.doc)
        id_ = str(uuid.uuid4())
        insert_response = crud.insert(
            object_=object_, id_=id_, session=self.session)
        assert isinstance(insert_response, str)
        assert insert_response == id_
        response_code = None
        try:
            delete_response = crud.delete(
                id_=id_, type_="otherClass", session=self.session)
        except Exception as e:
            error = e.get_HTTP()
        assert 400 == error.code

    def test_delete_id(self):
        """Test CRUD delete when wrong/undefined ID is given."""
        object_ = gen_dummy_object(random.choice(
            self.doc_collection_classes), self.doc)
        id_ = str(uuid.uuid4())
        insert_response = crud.insert(
            object_=object_, id_=id_, session=self.session)
        response_code = None
        try:
            delete_response = crud.delete(
                id_=999, type_=object_["@type"], session=self.session)
        except Exception as e:
            error = e.get_HTTP()
        assert 404 == error.code
        assert isinstance(insert_response, str)
        assert insert_response == id_

    def test_insert_type(self):
        """Test CRUD insert when wrong/undefined class is given."""
        object_ = gen_dummy_object(random.choice(
            self.doc_collection_classes), self.doc)
        id_ = str(uuid.uuid4())
        object_["@type"] = "otherClass"
        response_code = None
        try:
            insert_response = crud.insert(
                object_=object_, id_=id_, session=self.session)
        except Exception as e:
            error = e.get_HTTP()
        assert 400 == error.code

    def test_insert_used_id(self):
        """Test CRUD insert when used ID is given."""
        object_ = gen_dummy_object(random.choice(
            self.doc_collection_classes), self.doc)
        id_ = str(uuid.uuid4())
        insert_response = crud.insert(
            object_=object_, id_=id_, session=self.session)
        response_code = None
        try:
            insert_response = crud.insert(
                object_=object_, id_=id_, session=self.session)
        except Exception as e:
            error = e.get_HTTP()
        assert 400 == error.code

    def test_insert_ids(self):
        """Test CRUD insert when multiple ID's are given """
        objects = list()
        ids = "{},{}".format(str(uuid.uuid4()), str(uuid.uuid4()))
        ids_list = ids.split(',')
        for index in range(len(ids_list)):
            object = gen_dummy_object(random.choice(
                self.doc_collection_classes), self.doc)
            objects.append(object)
        insert_response = crud.insert_multiple(
            objects_=objects, session=self.session, id_=ids)
        for id_ in ids_list:
            assert id_ in insert_response

    def test_delete_ids(self):
        objects = list()
        ids = "{},{}".format(str(uuid.uuid4()), str(uuid.uuid4()))
        for index in range(len(ids.split(','))):
            object = gen_dummy_object(random.choice(
                self.doc_collection_classes), self.doc)
            objects.append(object)
        insert_response = crud.insert_multiple(objects_=objects,
                                               session=self.session, id_=ids)
        delete_response = crud.delete_multiple(
            id_=ids, type_=objects[0]["@type"], session=self.session)

        response_code = None
        id_list = ids.split(',')
        try:
            for index in range(len(id_list)):
                get_response = crud.get(
                    id_=id_list[index],
                    type_=objects[index]["@type"],
                    session=self.session,
                    api_name="api")
        except Exception as e:
            error = e.get_HTTP()
        assert 404 == error.code

    @classmethod
    def tearDownClass(self):
        """Undo the setUp steps for the Class."""
        self.session.close()


if __name__ == '__main__':
    unittest.main()
