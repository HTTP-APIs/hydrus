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
from hydra_python_core.doc_writer import HydraLink

import random
from typing import List
import string


def gen_dummy_object(class_title, doc):
    """Create a dummy object based on the definitions in the API Doc.
    :param class_title: Title of the class whose object is being created.
    :param doc: ApiDoc.
    :return: A dummy object of class `class_title`.
    """
    object_ = {
        "@type": class_title
    }
    for class_path in doc.parsed_classes:
        if class_title == doc.parsed_classes[class_path]["class"].title:
            for prop in doc.parsed_classes[class_path]["class"].supportedProperty:
                if isinstance(prop.prop, HydraLink) or prop.write is False:
                    continue
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
                if isinstance(prop.prop, HydraLink) or "vocab:" in prop.prop:
                    link_props = {}
                    dummy_obj = gen_dummy_object(class_, self.doc)
                    if isinstance(prop.prop, HydraLink):
                        nested_class = prop.prop.range.replace("vocab:", "")
                        for collection_path in self.doc.collections:
                            coll_class = self.doc.collections[
                                collection_path]['collection'].class_.title
                            if nested_class == coll_class:
                                id_ = str(uuid.uuid4())
                                crud.insert(
                                    gen_dummy_object(nested_class, self.doc),
                                    id_=id_,
                                    session=self.session)
                                link_props[prop.title] = id_
                                dummy_obj[prop.title] = f"{self.API_NAME}/{collection_path}/{id_}"
                    else:
                        nested_class = prop.prop.replace("vocab:", "")
                    obj_id = str(uuid.uuid4())
                    response = crud.insert(object_=dummy_obj, id_=obj_id,
                                           link_props=link_props, session=self.session)
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
                if isinstance(prop.prop, HydraLink):
                    continue
                # Find nested object so we can test searching of elements by
                # properties of nested objects.
                if "vocab:" in prop.prop:
                    object_ = gen_dummy_object(class_, self.doc)
                    # Setting property of a nested object as target
                    for property_ in object_[prop.title]:
                        if property_ != "@type":
                            object_[prop.title][property_] = "target_1"
                            target_property_1 = f"{prop.title}[{property_}]"
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
                    search_result = crud.get_collection(API_NAME="api", type_=class_,
                                                        session=self.session, paginate=True,
                                                        page_size=5, search_params=search_params)
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
            response_code = error.code
        assert 404 == response_code

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
            response_code = error.code
        assert 404 == response_code

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
            response_code = error.code
        assert 400 == response_code

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
            response_code = error.code
        assert 404 == response_code
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
            response_code = error.code
        assert 400 == response_code

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
            response_code = error.code
        assert 400 == response_code

    def test_insert_ids(self):
        """Test CRUD insert when multiple ID's are given """
        objects = list()
        ids = f"{str(uuid.uuid4())},{str(uuid.uuid4())}"
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
        ids = f"{str(uuid.uuid4())},{str(uuid.uuid4())}"
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
            response_code = error.code
        assert 404 == response_code

    @classmethod
    def tearDownClass(self):
        """Undo the setUp steps for the Class."""
        self.session.close()


if __name__ == '__main__':
    unittest.main()
