"""Try authorization on all possible URIs on the server."""

import json
import unittest
from hydrus.app_factory import app_factory
from hydrus.utils import set_session, set_doc, set_api_name, set_authentication, set_token
from hydrus.data import doc_parse
from hydra_python_core import doc_maker
from hydrus.samples import doc_writer_sample
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from hydrus.data.db_models import Base
from hydrus.data.user import add_user
from base64 import b64encode


# response = requests.get("http://127.0.0.1:8080/serverapi/CommandCollection",
#  headers={'Authorization':'Basic QWxhZGRpbjpPcGVuU2VzYW1l'})


class AuthTestCase(unittest.TestCase):
    """Test Class for the app."""

    @classmethod
    def setUpClass(self):
        """Database setup before the tests."""
        print("Creating a temporary datatbase...")
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        session = scoped_session(sessionmaker(bind=engine))

        self.session = session
        self.API_NAME = "demoapi"
        self.HYDRUS_SERVER_URL = "http://hydrus.com/"
        self.app = app_factory(self.API_NAME)
        self.doc = doc_maker.create_doc(
            doc_writer_sample.api_doc.generate(), self.HYDRUS_SERVER_URL, self.API_NAME)

        test_classes = doc_parse.get_classes(self.doc.generate())
        test_properties = doc_parse.get_all_properties(test_classes)
        doc_parse.insert_classes(test_classes, self.session)
        doc_parse.insert_properties(test_properties, self.session)
        add_user(1, "test", self.session)
        self.auth_header = {"X-Authentication": "",
                            "Authorization": "Basic {}".format(
                                b64encode(b"1:test").decode("ascii"))}
        self.wrong_id = {"X-Authentication": "",
                         "Authorization": "Basic {}".format(b64encode(b"2:test").decode("ascii"))}
        self.wrong_pass = {"X-Authentication": "",
                           "Authorization": "Basic {}".format(
                               b64encode(b"1:test2").decode("ascii"))}
        print("Classes, Properties and Users added successfully.")

        print("Setting up Hydrus utilities... ")
        self.api_name_util = set_api_name(self.app, self.API_NAME)
        self.session_util = set_session(self.app, self.session)
        self.doc_util = set_doc(self.app, self.doc)
        self.auth_util = set_authentication(self.app, True)
        self.token_util = set_token(self.app, False)
        self.client = self.app.test_client()

        print("Creating utilities context... ")
        self.api_name_util.__enter__()
        self.session_util.__enter__()
        self.doc_util.__enter__()
        self.auth_util.__enter__()
        self.token_util.__enter__()
        self.client.__enter__()

        print("Setup done, running tests...")

    @classmethod
    def tearDownClass(self):
        """Tear down temporary database and exit utilities"""
        self.client.__exit__(None, None, None)
        self.auth_util.__exit__(None, None, None)
        self.token_util.__exit__(None, None, None)
        self.doc_util.__exit__(None, None, None)
        self.session_util.__exit__(None, None, None)
        self.api_name_util.__exit__(None, None, None)
        self.session.close()

    def test_wrongID_GET(self):
        """Test for the index."""
        response_get = self.client.get("/{}".format(self.API_NAME))
        endpoints = json.loads(response_get.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint in self.doc.collections:
                response_get = self.client.get(endpoints[endpoint])
                self.wrong_id['X-Authentication'] = response_get.headers['X-Authentication']
                response_get = self.client.get(
                    endpoints[endpoint], headers=self.wrong_id)
                assert response_get.status_code == 401 or response_get.status_code == 400

    def test_wrongID_POST(self):
        """Test for the index."""
        response_get = self.client.get("/{}".format(self.API_NAME))
        endpoints = json.loads(response_get.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint in self.doc.collections:
                response_get = self.client.get(endpoints[endpoint])
                self.wrong_id['X-Authentication'] = response_get.headers['X-Authentication']
                response_get = self.client.post(
                    endpoints[endpoint], headers=self.wrong_id, data=json.dumps(dict(foo="bar")))
                assert response_get.status_code == 401 or response_get.status_code == 400

    def test_wrongPass_GET(self):
        """Test for the index."""
        response_get = self.client.get("/{}".format(self.API_NAME))
        endpoints = json.loads(response_get.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint in self.doc.collections:
                response_get = self.client.get(endpoints[endpoint])
                self.wrong_pass['X-Authentication'] = response_get.headers['X-Authentication']
                response_get = self.client.get(
                    endpoints[endpoint], headers=self.wrong_pass)
                assert response_get.status_code == 401

    def test_wrongPass_POST(self):
        """Test for the index."""
        response_get = self.client.get("/{}".format(self.API_NAME))
        endpoints = json.loads(response_get.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint in self.doc.collections:
                response_get = self.client.get(endpoints[endpoint])
                self.wrong_pass['X-Authentication'] = response_get.headers['X-Authentication']
                response_get = self.client.post(
                    endpoints[endpoint], headers=self.wrong_pass, data=json.dumps(dict(foo="bar")))
                assert response_get.status_code == 401

    def test_wrong_nonce_get(self):
        """Test for the index."""
        response_get = self.client.get("/{}".format(self.API_NAME))
        endpoints = json.loads(response_get.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint in self.doc.collections:
                self.auth_header['X-authentication'] = "random-string"
                response_get = self.client.get(
                    endpoints[endpoint], headers=self.auth_header)
                assert response_get.status_code == 401

    def test_wrong_nonce_post(self):
        """Test for the index."""
        response_get = self.client.get("/{}".format(self.API_NAME))
        endpoints = json.loads(response_get.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint in self.doc.collections:
                self.auth_header['X-authentication'] = "random-string"
                response_get = self.client.post(
                    endpoints[endpoint], headers=self.auth_header, data=json.dumps(dict(foo="bar")))
                assert response_get.status_code == 401

    def test_Auth_GET(self):
        """Test for the index."""
        response_get = self.client.get("/{}".format(self.API_NAME))
        endpoints = json.loads(response_get.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint in self.doc.collections:
                response_get = self.client.get(endpoints[endpoint])
                self.auth_header['X-Authentication'] = response_get.headers['X-Authentication']
                response_get = self.client.get(
                    endpoints[endpoint], headers=self.auth_header)
                assert response_get.status_code != 401

    def test_Auth_POST(self):
        """Test for the index."""
        response_get = self.client.get("/{}".format(self.API_NAME))
        endpoints = json.loads(response_get.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint in self.doc.collections:
                response_get = self.client.get(endpoints[endpoint])
                self.auth_header['X-Authentication'] = response_get.headers['X-Authentication']
                response_get = self.client.post(
                    endpoints[endpoint], headers=self.auth_header, data=json.dumps(dict(foo="bar")))
                assert response_get.status_code != 401

    def test_Auth_PUT(self):
        """Test for the index."""
        response_get = self.client.get("/{}".format(self.API_NAME))
        endpoints = json.loads(response_get.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint in self.doc.collections:
                response_get = self.client.get(endpoints[endpoint])
                self.auth_header['X-Authentication'] = response_get.headers['X-Authentication']
                response_get = self.client.put(
                    endpoints[endpoint], headers=self.auth_header, data=json.dumps(dict(foo="bar")))
                assert response_get.status_code != 401

    def test_Auth_DELETE(self):
        """Test for the index."""
        response_get = self.client.get("/{}".format(self.API_NAME))
        endpoints = json.loads(response_get.data.decode('utf-8'))
        for endpoint in endpoints:
            if endpoint in self.doc.collections:
                response_get = self.client.get(endpoints[endpoint])
                self.auth_header['X-Authentication'] = response_get.headers['X-Authentication']
                response_get = self.client.delete(
                    endpoints[endpoint], headers=self.auth_header)
                assert response_get.status_code != 401


if __name__ == '__main__':
    message = """
    Running tests for authorization. Checking if all responses are in proper order.
    """
    print(message)
    unittest.main()
