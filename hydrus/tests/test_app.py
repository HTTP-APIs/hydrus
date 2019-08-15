"""Test for checking if the response format is proper. Run test_crud before running this."""
import unittest
import random
import string
import json
import re
import uuid
from hydrus.app_factory import app_factory
from hydrus.socketio_factory import create_socket
from hydrus.utils import set_session, set_doc, set_api_name, set_page_size
from hydrus.data import doc_parse, crud
from hydra_python_core import doc_maker
from hydra_python_core.doc_writer import HydraLink
from hydrus.samples import doc_writer_sample
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from hydrus.data.db_models import Base


def gen_dummy_object(class_, doc):
    """Create a dummy object based on the definitions in the API Doc."""
    object_ = {
        "@type": class_
    }
    if class_ in doc.parsed_classes:
        for prop in doc.parsed_classes[class_]["class"].supportedProperty:
            # Skip properties which are not writeable
            if prop.write is False:
                continue
            if isinstance(prop.prop, HydraLink):
                continue
            if "vocab:" in prop.prop:
                prop_class = prop.prop.replace("vocab:", "")
                object_[prop.title] = gen_dummy_object(prop_class, doc)
            else:
                object_[prop.title] = ''.join(random.choice(
                    string.ascii_uppercase + string.digits) for _ in range(6))
        return object_


class ViewsTestCase(unittest.TestCase):
    """Test Class for the app."""

    @classmethod
    def setUpClass(self):
        """Database setup before the tests."""
        print("Creating a temporary database...")
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        session = scoped_session(sessionmaker(bind=engine))

        self.session = session
        self.API_NAME = "demoapi"
        self.page_size = 1
        self.HYDRUS_SERVER_URL = "http://hydrus.com/"

        self.app = app_factory(self.API_NAME)
        self.socketio = create_socket(self.app, self.session)
        print("going for create doc")

        self.doc = doc_maker.create_doc(
            doc_writer_sample.api_doc.generate(),
            self.HYDRUS_SERVER_URL,
            self.API_NAME)
        test_classes = doc_parse.get_classes(self.doc.generate())
        test_properties = doc_parse.get_all_properties(test_classes)
        doc_parse.insert_classes(test_classes, self.session)
        doc_parse.insert_properties(test_properties, self.session)

        print("Classes and properties added successfully.")

        print("Setting up hydrus utilities... ")
        self.api_name_util = set_api_name(self.app, self.API_NAME)
        self.session_util = set_session(self.app, self.session)
        self.doc_util = set_doc(self.app, self.doc)
        self.page_size_util = set_page_size(self.app, self.page_size)
        self.client = self.app.test_client()

        print("Creating utilities context... ")
        self.api_name_util.__enter__()
        self.session_util.__enter__()
        self.doc_util.__enter__()
        self.client.__enter__()

        print("Setup done, running tests...")

    @classmethod
    def tearDownClass(self):
        """Tear down temporary database and exit utilities"""
        self.client.__exit__(None, None, None)
        self.doc_util.__exit__(None, None, None)
        self.session_util.__exit__(None, None, None)
        self.api_name_util.__exit__(None, None, None)
        self.session.close()

    def setUp(self):
        for class_ in self.doc.parsed_classes:
            link_props = {}
            dummy_obj = gen_dummy_object(class_, self.doc)
            for supportedProp in self.doc.parsed_classes[class_]['class'].supportedProperty:
                if isinstance(supportedProp.prop, HydraLink):
                    class_name = supportedProp.prop.range.replace("vocab:", "")
                    for collection_path in self.doc.collections:
                        coll_class = self.doc.collections[
                            collection_path]['collection'].class_.title
                        if class_name == coll_class:
                            id_ = str(uuid.uuid4())
                            crud.insert(
                                gen_dummy_object(class_name, self.doc),
                                id_=id_,
                                session=self.session)
                            link_props[supportedProp.title] = id_
                            dummy_obj[supportedProp.title] = "{}/{}/{}".format(
                                self.API_NAME, collection_path, id_)
            crud.insert(
                dummy_obj,
                id_=str(
                    uuid.uuid4()),
                link_props=link_props,
                session=self.session)
            # If it's a collection class then add an extra object so
            # we can test pagination thoroughly.
            if class_ in self.doc.collections:
                crud.insert(
                    dummy_obj,
                    id_=str(
                        uuid.uuid4()),
                    session=self.session)

    def test_Index(self):
        """Test for the index."""
        response_get = self.client.get("/{}".format(self.API_NAME))
        endpoints = json.loads(response_get.data.decode('utf-8'))
        response_post = self.client.post(
            "/{}".format(self.API_NAME), data=dict(foo="bar"))
        response_put = self.client.put(
            "/{}".format(self.API_NAME), data=dict(foo="bar"))
        response_delete = self.client.delete("/{}".format(self.API_NAME))
        assert "@context" in endpoints
        assert endpoints["@id"] == "/{}".format(self.API_NAME)
        assert endpoints["@type"] == "EntryPoint"
        assert response_get.status_code == 200
        assert response_post.status_code == 405
        assert response_put.status_code == 405
        assert response_delete.status_code == 405

    def test_EntryPoint_context(self):
        """Test for the EntryPoint context."""
        response_get = self.client.get(
            "/{}/contexts/EntryPoint.jsonld".format(self.API_NAME))
        response_get_data = json.loads(response_get.data.decode('utf-8'))
        response_post = self.client.post(
            "/{}/contexts/EntryPoint.jsonld".format(self.API_NAME), data={})
        response_delete = self.client.delete(
            "/{}/contexts/EntryPoint.jsonld".format(self.API_NAME))
        assert response_get.status_code == 200
        assert "@context" in response_get_data
        assert response_post.status_code == 405
        assert response_delete.status_code == 405

    def test_Vocab(self):
        """Test the vocab."""
        response_get = self.client.get("/{}/vocab#".format(self.API_NAME))
        response_get_data = json.loads(response_get.data.decode('utf-8'))

        assert "@context" in response_get_data
        assert response_get_data["@type"] == "ApiDocumentation"
        assert response_get_data["@id"] == "{}{}/vocab".format(
            self.HYDRUS_SERVER_URL, self.API_NAME)
        assert response_get.status_code == 200

        response_delete = self.client.delete(
            "/{}/vocab#".format(self.API_NAME))
        assert response_delete.status_code == 405

        response_put = self.client.put(
            "/{}/vocab#".format(self.API_NAME), data=json.dumps(dict(foo='bar')))
        assert response_put.status_code == 405

        response_post = self.client.post(
            "/{}/vocab#".format(self.API_NAME), data=json.dumps(dict(foo='bar')))
        assert response_post.status_code == 405

    def test_Collections_GET(self):
        """Test GET on collection endpoints."""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            collection_name = "/".join(endpoints[endpoint].split(
                "/{}/".format(self.API_NAME))[1:])
            if collection_name in self.doc.collections:
                response_get = self.client.get(endpoints[endpoint])
                # pdb.set_trace()
                assert response_get.status_code == 200
                response_get_data = json.loads(
                    response_get.data.decode('utf-8'))
                assert "@context" in response_get_data
                assert "@id" in response_get_data
                assert "@type" in response_get_data
                assert "members" in response_get_data
                # Check the item URI has the valid format, so it can be dereferenced
                if len(response_get_data["members"]) > 0:
                    for item in response_get_data["members"]:
                        class_type = item["@type"]
                        if class_type in self.doc.parsed_classes:
                            class_ = self.doc.parsed_classes[class_type]["class"]
                            class_methods = [
                                x.method for x in class_.supportedOperation]
                            if "GET" in class_methods:
                                item_response = self.client.get(
                                    response_get_data["members"][0]["@id"])
                                assert item_response.status_code == 200

    def test_pagination(self):
        """Test basic pagination"""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            collection_name = "/".join(endpoints[endpoint].split(
                "/{}/".format(self.API_NAME))[1:])
            if collection_name in self.doc.collections:
                response_get = self.client.get(endpoints[endpoint])
                assert response_get.status_code == 200
                response_get_data = json.loads(
                    response_get.data.decode('utf-8'))
                assert "view" in response_get_data
                assert "first" in response_get_data["view"]
                assert "last" in response_get_data["view"]
                if "next" in response_get_data["view"]:
                    response_next = self.client.get(response_get_data["view"]["next"])
                    assert response_next.status_code == 200
                    response_next_data = json.loads(
                        response_next.data.decode('utf-8'))
                    assert "previous" in response_next_data["view"]
                break

    def test_Collections_PUT(self):
        """Test insert data to the collection."""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            collection_name = "/".join(endpoints[endpoint].split(
                "/{}/".format(self.API_NAME))[1:])
            if collection_name in self.doc.collections:
                collection = self.doc.collections[collection_name]["collection"]
                dummy_object = gen_dummy_object(
                    collection.class_.title, self.doc)
                good_response_put = self.client.put(
                    endpoints[endpoint], data=json.dumps(dummy_object))
                assert good_response_put.status_code == 201

    def test_object_POST(self):
        """Test replace of a given object using ID."""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            collection_name = "/".join(endpoints[endpoint].split(
                "/{}/".format(self.API_NAME))[1:])
            if collection_name in self.doc.collections:
                collection = self.doc.collections[collection_name]["collection"]
                class_ = self.doc.parsed_classes[collection.class_.title]["class"]
                class_methods = [x.method for x in class_.supportedOperation]
                dummy_object = gen_dummy_object(
                    collection.class_.title, self.doc)
                initial_put_response = self.client.put(
                    endpoints[endpoint], data=json.dumps(dummy_object))
                assert initial_put_response.status_code == 201
                response = json.loads(
                    initial_put_response.data.decode('utf-8'))
                regex = r'(.*)ID (.{36})* (.*)'
                matchObj = re.match(regex, response["description"])
                assert matchObj is not None
                id_ = matchObj.group(2)
                if "POST" in class_methods:
                    dummy_object = gen_dummy_object(
                        collection.class_.title, self.doc)
                    post_replace_response = self.client.post(
                        '{}/{}'.format(endpoints[endpoint], id_), data=json.dumps(dummy_object))
                    assert post_replace_response.status_code == 200

    def test_object_DELETE(self):
        """Test DELETE of a given object using ID."""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            collection_name = "/".join(endpoints[endpoint].split(
                "/{}/".format(self.API_NAME))[1:])
            if collection_name in self.doc.collections:
                collection = self.doc.collections[collection_name]["collection"]
                class_ = self.doc.parsed_classes[collection.class_.title]["class"]
                class_methods = [x.method for x in class_.supportedOperation]
                dummy_object = gen_dummy_object(
                    collection.class_.title, self.doc)
                initial_put_response = self.client.put(
                    endpoints[endpoint], data=json.dumps(dummy_object))
                assert initial_put_response.status_code == 201
                response = json.loads(
                    initial_put_response.data.decode('utf-8'))
                regex = r'(.*)ID (.{36})* (.*)'
                matchObj = re.match(regex, response["description"])
                assert matchObj is not None
                id_ = matchObj.group(2)
                if "DELETE" in class_methods:
                    delete_response = self.client.delete(
                        '{}/{}'.format(endpoints[endpoint], id_))
                    assert delete_response.status_code == 200

    def test_object_PUT_at_id(self):
        """Create object in collection using PUT at specific ID."""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            collection_name = "/".join(endpoints[endpoint].split(
                "/{}/".format(self.API_NAME))[1:])
            if collection_name in self.doc.collections:
                collection = self.doc.collections[collection_name]["collection"]
                class_ = self.doc.parsed_classes[collection.class_.title]["class"]
                class_methods = [x.method for x in class_.supportedOperation]
                dummy_object = gen_dummy_object(
                    collection.class_.title, self.doc)
                if "PUT" in class_methods:
                    dummy_object = gen_dummy_object(
                        collection.class_.title, self.doc)
                    put_response = self.client.put('{}/{}'.format(
                        endpoints[endpoint], uuid.uuid4()), data=json.dumps(dummy_object))
                    assert put_response.status_code == 201

    def test_object_PUT_at_ids(self):
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            collection_name = "/".join(endpoints[endpoint].split(
                "/{}/".format(self.API_NAME))[1:])
            if collection_name in self.doc.collections:
                collection = self.doc.collections[collection_name]["collection"]
                class_ = self.doc.parsed_classes[collection.class_.title]["class"]
                class_methods = [x.method for x in class_.supportedOperation]
                data_ = {"data": list()}
                objects = list()
                ids = ""
                for index in range(3):
                    objects.append(gen_dummy_object(
                        collection.class_.title, self.doc))
                    ids = "{},".format(uuid.uuid4())
                data_["data"] = objects
                if "PUT" in class_methods:
                    put_response = self.client.put(
                        '{}/add/{}'.format(endpoints[endpoint], ids),
                        data=json.dumps(data_))
                    assert put_response.status_code == 201

    def test_endpointClass_PUT(self):
        """Check non collection Class PUT."""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ["@context", "@id", "@type"]:
                class_name = "/".join(endpoints[endpoint].split(
                    "/{}/".format(self.API_NAME))[1:])
                if class_name not in self.doc.collections:
                    class_ = self.doc.parsed_classes[class_name]["class"]
                    class_methods = [
                        x.method for x in class_.supportedOperation]
                    if "PUT" in class_methods:
                        dummy_object = gen_dummy_object(class_.title, self.doc)
                        put_response = self.client.put(
                            endpoints[class_name], data=json.dumps(dummy_object))
                        assert put_response.status_code == 201

    def test_endpointClass_POST(self):
        """Check non collection Class POST."""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ["@context", "@id", "@type"]:
                class_name = "/".join(endpoints[endpoint].split(
                    "/{}/".format(self.API_NAME))[1:])
                if class_name not in self.doc.collections:
                    class_ = self.doc.parsed_classes[class_name]["class"]
                    class_methods = [
                        x.method for x in class_.supportedOperation]
                    if "POST" in class_methods:
                        dummy_object = gen_dummy_object(class_.title, self.doc)
                        post_response = self.client.post(
                            endpoints[class_name], data=json.dumps(dummy_object))
                        assert post_response.status_code == 200

    def test_endpointClass_DELETE(self):
        """Check non collection Class DELETE."""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ["@context", "@id", "@type"]:
                class_name = "/".join(endpoints[endpoint].split(
                    "/{}/".format(self.API_NAME))[1:])
                if class_name not in self.doc.collections:
                    class_ = self.doc.parsed_classes[class_name]["class"]
                    class_methods = [
                        x.method for x in class_.supportedOperation]
                    if "DELETE" in class_methods:
                        delete_response = self.client.delete(
                            endpoints[class_name])
                        assert delete_response.status_code == 200

    def test_endpointClass_GET(self):
        """Check non collection Class GET."""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ["@context", "@id", "@type"]:
                class_name = "/".join(endpoints[endpoint].split(
                    "/{}/".format(self.API_NAME))[1:])
                if class_name not in self.doc.collections:
                    class_ = self.doc.parsed_classes[class_name]["class"]
                    class_methods = [
                        x.method for x in class_.supportedOperation]
                    if "GET" in class_methods:
                        response_get = self.client.get(endpoints[class_name])
                        assert response_get.status_code == 200
                        response_get_data = json.loads(
                            response_get.data.decode('utf-8'))
                        assert "@context" in response_get_data
                        assert "@id" in response_get_data
                        assert "@type" in response_get_data

    def test_IriTemplate(self):
        """Test structure of IriTemplates attached to collections"""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            collection_name = "/".join(endpoints[endpoint].split(
                "/{}/".format(self.API_NAME))[1:])
            if collection_name in self.doc.collections:
                response_get = self.client.get(endpoints[endpoint])
                assert response_get.status_code == 200
                response_get_data = json.loads(
                    response_get.data.decode('utf-8'))
                assert "search" in response_get_data
                assert "mapping" in response_get_data["search"]
                collection = self.doc.collections[collection_name]["collection"]
                class_ = self.doc.parsed_classes[collection.class_.title]["class"]
                class_props = [x.prop for x in class_.supportedProperty]
                for mapping in response_get_data["search"]["mapping"]:
                    if mapping["property"] not in ["limit", "offset", "pageIndex"]:
                        assert mapping["property"] in class_props

    def test_client_controlled_pagination(self):
        """Test pagination controlled by client with help of pageIndex,
        offset and limit parameters."""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            collection_name = "/".join(endpoints[endpoint].split(
                "/{}/".format(self.API_NAME))[1:])
            if collection_name in self.doc.collections:
                response_get = self.client.get(endpoints[endpoint])
                assert response_get.status_code == 200
                response_get_data = json.loads(
                    response_get.data.decode('utf-8'))
                assert "search" in response_get_data
                assert "mapping" in response_get_data["search"]
                # Test with pageIndex and limit
                params = {"pageIndex": 1, "limit": 2}
                response_for_page_param = self.client.get(endpoints[endpoint], query_string=params)
                assert response_for_page_param.status_code == 200
                response_for_page_param_data = json.loads(
                    response_for_page_param.data.decode('utf-8'))
                assert "first" in response_for_page_param_data["view"]
                assert "last" in response_for_page_param_data["view"]
                if "next" in response_for_page_param_data["view"]:
                    assert "pageIndex=2" in response_for_page_param_data["view"]["next"]
                    next_response = self.client.get(response_for_page_param_data["view"]["next"])
                    assert next_response.status_code == 200
                    next_response_data = json.loads(
                        next_response.data.decode('utf-8'))
                    assert "previous" in next_response_data["view"]
                    assert "pageIndex=1" in next_response_data["view"]["previous"]
                    # Test with offset and limit
                    params = {"offset": 1, "limit": 2}
                    response_for_offset_param = self.client.get(endpoints[endpoint],
                                                                query_string=params)
                    assert response_for_offset_param.status_code == 200
                    response_for_offset_param_data = json.loads(
                        response_for_offset_param.data.decode('utf-8'))
                    assert "first" in response_for_offset_param_data["view"]
                    assert "last" in response_for_offset_param_data["view"]
                    if "next" in response_for_offset_param_data["view"]:
                        assert "offset=3" in response_for_offset_param_data["view"]["next"]
                        next_response = self.client.get(
                            response_for_offset_param_data["view"]["next"])
                        assert next_response.status_code == 200
                        next_response_data = json.loads(
                            next_response.data.decode('utf-8'))
                        assert "previous" in next_response_data["view"]
                        assert "offset=1" in next_response_data["view"]["previous"]

    def test_GET_for_nested_class(self):
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ["@context", "@id", "@type"]:
                class_name = "/".join(endpoints[endpoint].split(
                    "/{}/".format(self.API_NAME))[1:])
                if class_name not in self.doc.collections:
                    class_ = self.doc.parsed_classes[class_name]["class"]
                    class_methods = [
                        x.method for x in class_.supportedOperation]
                    if "GET" in class_methods:
                        response_get = self.client.get(endpoints[class_name])
                        assert response_get.status_code == 200
                        response_get_data = json.loads(
                            response_get.data.decode('utf-8'))
                        assert "@context" in response_get_data
                        assert "@id" in response_get_data
                        assert "@type" in response_get_data
                        class_props = [x for x in class_.supportedProperty]
                        for prop_name in class_props:
                            if isinstance(prop_name.prop, HydraLink) and prop_name.read is True:
                                nested_obj_resp = self.client.get(
                                    response_get_data[prop_name.title])
                                assert nested_obj_resp.status_code == 200
                                nested_obj = json.loads(
                                    nested_obj_resp.data.decode('utf-8'))
                                assert "@type" in nested_obj
                            elif "vocab:" in prop_name.prop:
                                assert "@type" in response_get_data[prop_name.title]

    def test_required_props(self):
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ["@context", "@id", "@type"]:
                class_name = "/".join(endpoints[endpoint].split(
                    "/{}/".format(self.API_NAME))[1:])
                if class_name not in self.doc.collections:
                    class_ = self.doc.parsed_classes[class_name]["class"]
                    class_methods = [
                        x.method for x in class_.supportedOperation]
                    if "PUT" in class_methods:
                        dummy_object = gen_dummy_object(class_.title, self.doc)
                        required_prop = ""
                        for prop in class_.supportedProperty:
                            if prop.required:
                                required_prop = prop.title
                                break
                        if required_prop:
                            del dummy_object[required_prop]
                            put_response = self.client.put(
                                endpoints[class_name], data=json.dumps(dummy_object))
                            assert put_response.status_code == 400

    def test_writeable_props(self):
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ["@context", "@id", "@type"]:
                class_name = "/".join(endpoints[endpoint].split(
                    "/{}/".format(self.API_NAME))[1:])
                if class_name not in self.doc.collections:
                    class_ = self.doc.parsed_classes[class_name]["class"]
                    class_methods = [
                        x.method for x in class_.supportedOperation]
                    if "POST" in class_methods:
                        dummy_object = gen_dummy_object(class_.title, self.doc)
                        # Test for writeable properties
                        post_response = self.client.post(
                            endpoints[class_name], data=json.dumps(dummy_object))
                        assert post_response.status_code == 200
                        # Test for properties with writeable=False
                        non_writeable_prop = ""
                        for prop in class_.supportedProperty:
                            if prop.write is False:
                                non_writeable_prop = prop.title
                                break
                        if non_writeable_prop != "":
                            dummy_object[non_writeable_prop] = "xyz"
                            post_response = self.client.post(
                                endpoints[class_name], data=json.dumps(dummy_object))
                            assert post_response.status_code == 405

    def test_readable_props(self):
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ["@context", "@id", "@type"]:
                class_name = "/".join(endpoints[endpoint].split(
                    "/{}/".format(self.API_NAME))[1:])
                if class_name not in self.doc.collections:
                    class_ = self.doc.parsed_classes[class_name]["class"]
                    class_methods = [
                        x.method for x in class_.supportedOperation]
                    if "GET" in class_methods:
                        not_readable_prop = ""
                        for prop in class_.supportedProperty:
                            if prop.read is False:
                                not_readable_prop = prop.title
                                break
                        if not_readable_prop:
                            get_response = self.client.get(
                                endpoints[class_name])
                            get_response_data = json.loads(
                                get_response.data.decode('utf-8'))
                            assert not_readable_prop not in get_response_data

    def test_bad_objects(self):
        """Checks if bad objects are added or not."""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            collection_name = "/".join(endpoints[endpoint].split(
                "/{}/".format(self.API_NAME))[1:])
            if collection_name in self.doc.collections:
                bad_response_put = self.client.put(
                    endpoints[endpoint],
                    data=json.dumps(
                        dict(
                            foo='bar')))
                assert bad_response_put.status_code == 400

    def test_bad_requests(self):
        """Checks if bad requests are handled or not."""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            collection_name = "/".join(endpoints[endpoint].split(
                "/{}/".format(self.API_NAME))[1:])
            if collection_name in self.doc.collections:
                collection = self.doc.collections[collection_name]["collection"]
                class_ = self.doc.parsed_classes[collection.class_.title]["class"]
                class_methods = [x.method for x in class_.supportedOperation]
                dummy_object = gen_dummy_object(
                    collection.class_.title, self.doc)
                initial_put_response = self.client.put(
                    endpoints[endpoint], data=json.dumps(dummy_object))
                assert initial_put_response.status_code == 201
                response = json.loads(
                    initial_put_response.data.decode('utf-8'))
                regex = r'(.*)ID (.{36})* (.*)'
                matchObj = re.match(regex, response["description"])
                assert matchObj is not None
                id_ = matchObj.group(2)
                if "POST" not in class_methods:
                    dummy_object = gen_dummy_object(
                        collection.class_.title, self.doc)
                    post_replace_response = self.client.post(
                        '{}/{}'.format(endpoints[endpoint], id_), data=json.dumps(dummy_object))
                    assert post_replace_response.status_code == 405
                if "DELETE" not in class_methods:
                    delete_response = self.client.delete(
                        '{}/{}'.format(endpoints[endpoint], id_))
                    assert delete_response.status_code == 405

    def test_Endpoints_Contexts(self):
        """Test all endpoints contexts are generated properly."""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            collection_name = "/".join(endpoints[endpoint].split(
                "/{}/".format(self.API_NAME))[1:])
            if collection_name in self.doc.collections:
                response_get = self.client.get(endpoints[endpoint])
                assert response_get.status_code == 200
                context = json.loads(
                    response_get.data.decode('utf-8'))["@context"]
                response_context = self.client.get(context)
                response_context_data = json.loads(
                    response_context.data.decode('utf-8'))
                assert response_context.status_code == 200
                assert "@context" in response_context_data


class SocketTestCase(unittest.TestCase):
    """Test Class for socket events and operations."""

    @classmethod
    def setUpClass(self):
        """Database setup before the tests."""
        print("Creating a temporary database...")
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        session = scoped_session(sessionmaker(bind=engine))

        self.session = session
        self.API_NAME = "demoapi"
        self.page_size = 1
        self.HYDRUS_SERVER_URL = "http://hydrus.com/"

        self.app = app_factory(self.API_NAME)
        self.socketio = create_socket(self.app, self.session)
        print("going for create doc")

        self.doc = doc_maker.create_doc(
            doc_writer_sample.api_doc.generate(),
            self.HYDRUS_SERVER_URL,
            self.API_NAME)
        test_classes = doc_parse.get_classes(self.doc.generate())
        test_properties = doc_parse.get_all_properties(test_classes)
        doc_parse.insert_classes(test_classes, self.session)
        doc_parse.insert_properties(test_properties, self.session)

        print("Classes and properties added successfully.")

        print("Setting up hydrus utilities... ")
        self.api_name_util = set_api_name(self.app, self.API_NAME)
        self.session_util = set_session(self.app, self.session)
        self.doc_util = set_doc(self.app, self.doc)
        self.page_size_util = set_page_size(self.app, self.page_size)
        self.client = self.app.test_client()
        self.socketio_client = self.socketio.test_client(self.app, namespace='/sync')

        print("Creating utilities context... ")
        self.api_name_util.__enter__()
        self.session_util.__enter__()
        self.doc_util.__enter__()
        self.client.__enter__()

        print("Setup done, running tests...")

    @classmethod
    def tearDownClass(self):
        """Tear down temporary database and exit utilities"""
        self.client.__exit__(None, None, None)
        self.doc_util.__exit__(None, None, None)
        self.session_util.__exit__(None, None, None)
        self.api_name_util.__exit__(None, None, None)
        self.session.close()

    def setUp(self):
        for class_ in self.doc.parsed_classes:
            dummy_obj = gen_dummy_object(class_, self.doc)
            crud.insert(
                dummy_obj,
                id_=str(
                    uuid.uuid4()),
                session=self.session)
            # If it's a collection class then add an extra object so
            # we can test pagination thoroughly.
            if class_ in self.doc.collections:
                crud.insert(
                    dummy_obj,
                    id_=str(
                        uuid.uuid4()),
                    session=self.session)
        # Add two dummy modification records
        crud.insert_modification_record(method="POST",
                                        resource_url="", session=self.session)
        crud.insert_modification_record(method="DELETE",
                                        resource_url="", session=self.session)

    def test_connect(self):
        """Test connect event."""
        socket_client = self.socketio.test_client(self.app, namespace='/sync')
        data = socket_client.get_received('/sync')
        assert len(data) > 0
        event = data[0]
        assert event['name'] == 'connect'
        last_job_id = crud.get_last_modification_job_id(self.session)
        assert event['args'][0]['last_job_id'] == last_job_id
        socket_client.disconnect(namespace='/sync')

    def test_reconnect(self):
        """Test reconnect event."""
        socket_client = self.socketio.test_client(self.app, namespace='/sync')
        # Flush data of first connect event
        socket_client.get_received('/sync')
        # Client reconnects by emitting 'reconnect' event.
        socket_client.emit('reconnect', namespace='/sync')
        # Get update received on reconnecting to the server
        data = socket_client.get_received('/sync')
        assert len(data) > 0
        # Extract the event information
        event = data[0]
        assert event['name'] == 'connect'
        last_job_id = crud.get_last_modification_job_id(self.session)
        # Check last job id with last_job_id received by client in the update.
        assert event['args'][0]['last_job_id'] == last_job_id
        socket_client.disconnect(namespace='/sync')

    def test_modification_table_diff(self):
        """Test 'modification-table-diff' events."""
        # Flush old received data at socket client
        self.socketio_client.get_received('/sync')
        # Set last_job_id as the agent_job_id
        agent_job_id = crud.get_last_modification_job_id(self.session)
        # Add an extra modification record newer than the agent_job_id
        new_latest_job_id = crud.insert_modification_record(method="POST",
                                                            resource_url="", session=self.session)
        self.socketio_client.emit('get_modification_table_diff',
                                  {'agent_job_id': agent_job_id}, namespace='/sync')
        data = self.socketio_client.get_received('/sync')
        assert len(data) > 0
        event = data[0]
        assert event['name'] == 'modification_table_diff'
        # Check received event contains data of newly added modification record.
        assert event['args'][0][0]['method'] == "POST"
        assert event['args'][0][0]['resource_url'] == ""
        assert event['args'][0][0]['job_id'] == new_latest_job_id

    def test_socketio_POST_updates(self):
        """Test 'update' event emitted by socketio for POST operations."""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ["@context", "@id", "@type"]:
                class_name = "/".join(endpoints[endpoint].split(
                    "/{}/".format(self.API_NAME))[1:])
                if class_name not in self.doc.collections:
                    class_ = self.doc.parsed_classes[class_name]["class"]
                    class_methods = [
                        x.method for x in class_.supportedOperation]
                    if "POST" in class_methods:
                        dummy_object = gen_dummy_object(class_.title, self.doc)
                        # Flush old socketio updates
                        self.socketio_client.get_received('/sync')
                        post_response = self.client.post(
                            endpoints[class_name], data=json.dumps(dummy_object))
                        assert post_response.status_code == 200
                        # Get new socketio update
                        update = self.socketio_client.get_received('/sync')
                        assert len(update) != 0
                        assert update[0]['args'][0]['method'] == "POST"
                        resource_name = update[0]['args'][0]['resource_url'].split('/')[-1]
                        assert resource_name == endpoints[class_name].split('/')[-1]

    def test_socketio_DELETE_updates(self):
        """Test 'update' event emitted by socketio for DELETE operations."""
        index = self.client.get("/{}".format(self.API_NAME))
        assert index.status_code == 200
        endpoints = json.loads(index.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint not in ["@context", "@id", "@type"]:
                class_name = "/".join(endpoints[endpoint].split(
                    "/{}/".format(self.API_NAME))[1:])
                if class_name not in self.doc.collections:
                    class_ = self.doc.parsed_classes[class_name]["class"]
                    class_methods = [
                        x.method for x in class_.supportedOperation]
                    if "DELETE" in class_methods:
                        # Flush old socketio updates
                        self.socketio_client.get_received('/sync')
                        delete_response = self.client.delete(
                            endpoints[class_name])
                        assert delete_response.status_code == 200
                        # Get new update event
                        update = self.socketio_client.get_received('/sync')
                        assert len(update) != 0
                        assert update[0]['args'][0]['method'] == 'DELETE'
                        resource_name = update[0]['args'][0]['resource_url'].split('/')[-1]
                        assert resource_name == endpoints[class_name].split('/')[-1]


if __name__ == '__main__':
    message = """
    Running tests for the app. Checking if all responses are in proper order.
    """
    unittest.main()
