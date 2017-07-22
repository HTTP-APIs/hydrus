"""Test for checking if the response format is proper. Run test_crud before running this."""
# -*- coding: utf-8 -*-

import unittest
import random
import string
import os
import json
import pdb
from hydrus.app import API_NAME, SERVER_URL, API_DOC, app, set_session
from hydrus.data import doc_parse
from hydrus.metadata.doc_gen import doc_gen
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hydrus.data.db_models import Base


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
                object_[prop.title] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        return object_


class ViewsTestCase(unittest.TestCase):
    """Test Class for the app."""

    @classmethod
    def setUpClass(self):
        """Database setup before the tests."""
        print("Creating a temporary datatbsse...")
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        self.session = session
        doc = doc_gen("test", "test")
        test_classes = doc_parse.get_classes(doc.generate())
        test_properties = doc_parse.get_all_properties(test_classes)
        doc_parse.insert_classes(test_classes, self.session)
        doc_parse.insert_properties(test_properties, self.session)
        print("Classes and properties added successfully.")
        print("Setup done, running tests...")

    @classmethod
    def tearDownClass(self):
        """Tear down temporary database."""
        self.session.close()

    def test_Index(self):
        """Test for the index."""
        with set_session(app, self.session):
            with app.test_client() as client:
                response_get = client.get("/"+API_NAME)
                endpoints = json.loads(response_get.data.decode('utf-8'))
                response_post = client.post("/"+API_NAME, data=dict(foo="bar"))
                response_put = client.put("/"+API_NAME, data=dict(foo="bar"))
                response_delete = client.delete("/"+API_NAME)
                assert "@context" in endpoints
                assert endpoints["@id"] == "/"+API_NAME
                assert endpoints["@type"] == "EntryPoint"
                assert response_get.status_code == 200
                assert response_post.status_code == 405
                assert response_put.status_code == 405
                assert response_delete.status_code == 405

    def test_EntryPoint_context(self):
        """Test for the EntryPoint context."""
        with set_session(app, self.session):
            with app.test_client() as client:
                response_get = client.get("/"+API_NAME + "/contexts/EntryPoint.jsonld")
                response_get_data = json.loads(response_get.data.decode('utf-8'))
                response_post = client.post("/"+API_NAME + "/contexts/EntryPoint.jsonld", data={})
                response_delete = client.delete("/"+API_NAME + "/contexts/EntryPoint.jsonld")
                assert response_get.status_code == 200
                assert "@context" in response_get_data
                assert response_post.status_code == 405
                assert response_delete.status_code == 405

    def test_Vocab(self):
        """Test the vocab."""
        with set_session(app, self.session):
            with app.test_client() as client:
                response_get = client.get("/"+API_NAME + "/vocab#")
                response_get_data = json.loads(response_get.data.decode('utf-8'))
                assert "@context" in response_get_data
                # print(response_get_data["@id"], SERVER_URL+API_NAME +"/vocab#")
                assert response_get_data["@type"] == "ApiDocumentation"
                assert response_get_data["@id"] == SERVER_URL+API_NAME+"/vocab"
                assert response_get.status_code == 200

                response_delete = client.delete("/"+API_NAME+"/vocab#")
                assert response_delete.status_code == 405

                response_put = client.put("/"+API_NAME+"/vocab#", data=json.dumps(dict(foo='bar')))
                assert response_put.status_code == 405

                response_post = client.post("/"+API_NAME+"/vocab#", data=json.dumps(dict(foo='bar')))
                assert response_post.status_code == 405

    def test_Collections_GET(self):
        """Test GET on collection endpoints."""
        with set_session(app, self.session):
            with app.test_client() as client:
                index = client.get("/"+API_NAME)
                assert index.status_code == 200
                endpoints = json.loads(index.data.decode('utf-8'))
                for endpoint in endpoints:
                    if endpoint in API_DOC.collections:
                        response_get = client.get(endpoints[endpoint])
                        assert response_get.status_code == 200
                        response_get_data = json.loads(response_get.data.decode('utf-8'))
                        assert "@context" in response_get_data
                        assert "@id" in response_get_data
                        assert "@type" in response_get_data
                        assert "members" in response_get_data

    def test_Collections_PUT(self):
        """Test insert data to the collection."""
        with set_session(app, self.session):
            with app.test_client() as client:
                index = client.get("/"+API_NAME)
                assert index.status_code == 200
                endpoints = json.loads(index.data.decode('utf-8'))
                for collection_name in endpoints:
                    if collection_name in API_DOC.collections:
                        collection = API_DOC.collections[collection_name]["collection"]
                        dummy_object = gen_dummy_object(collection.class_.title, API_DOC)
                        good_response_put = client.put(endpoints[collection_name], data=json.dumps(dummy_object))
                        assert good_response_put.status_code == 201

    def test_object_POST(self):
        """Test replace of a given object using ID."""
        with set_session(app, self.session):
            with app.test_client() as client:
                index = client.get("/"+API_NAME)
                assert index.status_code == 200
                endpoints = json.loads(index.data.decode('utf-8'))
                for collection_name in endpoints:
                    if collection_name in API_DOC.collections:
                        collection = API_DOC.collections[collection_name]["collection"]
                        class_ = API_DOC.parsed_classes[collection.class_.title]["class"]
                        class_methods = [x.method for x in class_.supportedOperation]
                        dummy_object = gen_dummy_object(collection.class_.title, API_DOC)
                        initial_put_response = client.put(endpoints[collection_name], data=json.dumps(dummy_object))
                        assert initial_put_response.status_code == 201
                        response = json.loads(initial_put_response.data.decode('utf-8'))
                        id_ = response["201"].split('=')[1]
                        if "POST" in class_methods:
                            dummy_object = gen_dummy_object(collection.class_.title, API_DOC)
                            post_replace_response = client.post(endpoints[collection_name]+'/'+str(id_), data=json.dumps(dummy_object))
                            assert post_replace_response.status_code == 200

    def test_object_DELETE(self):
        """Test DELETE of a given object using ID."""
        with set_session(app, self.session):
            with app.test_client() as client:
                index = client.get("/"+API_NAME)
                assert index.status_code == 200
                endpoints = json.loads(index.data.decode('utf-8'))
                for collection_name in endpoints:
                    if collection_name in API_DOC.collections:
                        collection = API_DOC.collections[collection_name]["collection"]
                        class_ = API_DOC.parsed_classes[collection.class_.title]["class"]
                        class_methods = [x.method for x in class_.supportedOperation]
                        dummy_object = gen_dummy_object(collection.class_.title, API_DOC)
                        initial_put_response = client.put(endpoints[collection_name], data=json.dumps(dummy_object))
                        assert initial_put_response.status_code == 201
                        response = json.loads(initial_put_response.data.decode('utf-8'))
                        id_ = response["201"].split('=')[1]
                        if "DELETE" in class_methods:
                            delete_response = client.delete(endpoints[collection_name]+'/'+str(id_))
                            assert delete_response.status_code == 200

    def test_Endpoints_Contexts(self):
        """Test all endpoints contexts are generated properly."""
        with set_session(app, self.session):
            with app.test_client() as client:
                index = client.get("/"+API_NAME)
                assert index.status_code == 200
                endpoints = json.loads(index.data.decode('utf-8'))
                for collection_name in endpoints:
                    if collection_name in API_DOC.collections:
                        response_get = client.get(endpoints[collection_name])
                        assert response_get.status_code == 200
                        context = json.loads(response_get.data.decode('utf-8'))["@context"]
                        response_context = client.get(context)
                        response_context_data = json.loads(response_context.data.decode('utf-8'))
                        assert response_context.status_code == 200
                        assert "@context" in response_context_data

    def test_object_PUT(self):
        """Create object at a specific ID where allowed."""
        with set_session(app, self.session):
            with app.test_client() as client:
                index = client.get("/"+API_NAME)
                assert index.status_code == 200
                endpoints = json.loads(index.data.decode('utf-8'))
                for collection_name in endpoints:
                    if collection_name in API_DOC.collections:
                        collection = API_DOC.collections[collection_name]["collection"]
                        class_ = API_DOC.parsed_classes[collection.class_.title]["class"]
                        class_methods = [x.method for x in class_.supportedOperation]
                        dummy_object = gen_dummy_object(collection.class_.title, API_DOC)
                        if "PUT" in class_methods:
                            dummy_object = gen_dummy_object(collection.class_.title, API_DOC)
                            put_response = client.put(endpoints[collection_name], data=json.dumps(dummy_object))
                            assert put_response.status_code == 201

    def test_endpointClass_PUT(self):
        """Create non collection Class using PUT."""
        with set_session(app, self.session):
            with app.test_client() as client:
                index = client.get("/"+API_NAME)
                assert index.status_code == 200
                endpoints = json.loads(index.data.decode('utf-8'))
                for class_name in endpoints:
                    if class_name not in API_DOC.collections and class_name not in ["@context", "@id", "@type"]:
                        class_ = API_DOC.parsed_classes[class_name]["class"]
                        class_methods = [x.method for x in class_.supportedOperation]
                        if "PUT" in class_methods:
                            dummy_object = gen_dummy_object(class_.title, API_DOC)
                            put_response = client.put(endpoints[class_name], data=json.dumps(dummy_object))
                            assert put_response.status_code == 201

    def test_endpointClass_POST(self):
        """Update non collection Class using PUT."""
        with set_session(app, self.session):
            with app.test_client() as client:
                index = client.get("/"+API_NAME)
                assert index.status_code == 200
                endpoints = json.loads(index.data.decode('utf-8'))
                for class_name in endpoints:
                    if class_name not in API_DOC.collections and class_name not in ["@context", "@id", "@type"]:
                        class_ = API_DOC.parsed_classes[class_name]["class"]
                        class_methods = [x.method for x in class_.supportedOperation]
                        if "POST" in class_methods:
                            dummy_object = gen_dummy_object(class_.title, API_DOC)
                            put_response = client.post(endpoints[class_name], data=json.dumps(dummy_object))
                            assert put_response.status_code == 201

    def test_endpointClass_DELETE(self):
        """Update non collection Class using PUT."""
        with set_session(app, self.session):
            with app.test_client() as client:
                index = client.get("/"+API_NAME)
                assert index.status_code == 200
                endpoints = json.loads(index.data.decode('utf-8'))
                for class_name in endpoints:
                    if class_name not in API_DOC.collections and class_name not in ["@context", "@id", "@type"]:
                        class_ = API_DOC.parsed_classes[class_name]["class"]
                        class_methods = [x.method for x in class_.supportedOperation]
                        if "DELETE" in class_methods:
                            put_response = client.delete(endpoints[class_name])
                            assert put_response.status_code == 200

    def test_endpointClass_DELETE(self):
        """Update non collection Class using PUT."""
        with set_session(app, self.session):
            with app.test_client() as client:
                index = client.get("/"+API_NAME)
                assert index.status_code == 200
                endpoints = json.loads(index.data.decode('utf-8'))
                for class_name in endpoints:
                    if class_name not in API_DOC.collections and class_name not in ["@context", "@id", "@type"]:
                        class_ = API_DOC.parsed_classes[class_name]["class"]
                        class_methods = [x.method for x in class_.supportedOperation]
                        if "GET" in class_methods:
                            response_get = client.get(endpoints[class_name])
                            assert response_get.status_code in [200, 404]
                            if response_get.status_code == 200:
                                response_get_data = json.loads(response_get.data.decode('utf-8'))
                                assert "@context" in response_get_data
                                assert "@id" in response_get_data
                                assert "@type" in response_get_data

    def test_bad_objects(self):
        """Checks if bad objects are added or not."""
        with set_session(app, self.session):
            with app.test_client() as client:
                index = client.get("/"+API_NAME)
                assert index.status_code == 200
                endpoints = json.loads(index.data.decode('utf-8'))
                for collection_name in endpoints:
                    if collection_name in API_DOC.collections:
                        bad_response_put = client.put(endpoints[collection_name], data=json.dumps(dict(foo='bar')))
                        assert bad_response_put.status_code == 400

    def test_bad_requests(self):
        """Checks if bad requests are handled or not."""
        with set_session(app, self.session):
            with app.test_client() as client:
                index = client.get("/"+API_NAME)
                assert index.status_code == 200
                endpoints = json.loads(index.data.decode('utf-8'))
                for collection_name in endpoints:
                    if collection_name in API_DOC.collections:
                        collection = API_DOC.collections[collection_name]["collection"]
                        class_ = API_DOC.parsed_classes[collection.class_.title]["class"]
                        class_methods = [x.method for x in class_.supportedOperation]
                        dummy_object = gen_dummy_object(collection.class_.title, API_DOC)
                        initial_put_response = client.put(endpoints[collection_name], data=json.dumps(dummy_object))
                        assert initial_put_response.status_code == 201
                        response = json.loads(initial_put_response.data.decode('utf-8'))
                        id_ = response["201"].split('=')[1]
                        if "POST" not in class_methods:
                            dummy_object = gen_dummy_object(collection.class_.title, API_DOC)
                            post_replace_response = client.post(endpoints[collection_name]+'/'+str(id_), data=json.dumps(dummy_object))
                            assert post_replace_response.status_code == 405


if __name__ == '__main__':
    message = """
    Running tests for the app. Checking if all responses are in proper order.
    """
    print(message)
    unittest.main()
