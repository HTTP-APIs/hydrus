"""Try authorization on all possible URIs on the server."""

from hydrus.data.user import generate_basic_digest
import json
import unittest
from hydrus.app import app_factory
from hydrus.utils import set_session, set_doc, set_api_name, set_authentication
from hydrus.data import doc_parse
from hydrus.hydraspec import doc_writer_sample, doc_maker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hydrus.data.db_models import Base
from hydrus.data.user import add_user


# response = requests.get("http://127.0.0.1:8080/serverapi/CommandCollection", headers={'Authorization':'Basic QWxhZGRpbjpPcGVuU2VzYW1l'})


class AuthTestCase(unittest.TestCase):
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
        self.API_NAME = "demoapi"
        self.HYDRUS_SERVER_URL = "http://hydrus.com/"
        self.app = app_factory(self.API_NAME)
        self.doc = doc_maker.create_doc(doc_writer_sample.api_doc.generate(), self.HYDRUS_SERVER_URL, self.API_NAME)

        test_classes = doc_parse.get_classes(self.doc.generate())
        test_properties = doc_parse.get_all_properties(test_classes)
        doc_parse.insert_classes(test_classes, self.session)
        doc_parse.insert_properties(test_properties, self.session)
        add_user(1, "test", self.session)
        self.auth_header = {"Authorization": "Basic " + generate_basic_digest(1, "test")}
        print("Classes, Properties and Users added successfully.")
        print("Setup done, running tests...")

    @classmethod
    def tearDownClass(self):
        """Tear down temporary database."""
        self.session.close()

    def test_Auth_GET(self):
        """Test for the index."""
        with set_api_name(self.app, self.API_NAME):
            with set_session(self.app, self.session):
                with set_doc(self.app, self.doc):
                    with set_authentication(self.app, True):
                        with self.app.test_client() as client:
                            response_get = client.get("/"+self.API_NAME)
                            endpoints = json.loads(response_get.data.decode('utf-8'))
                            for endpoint in endpoints:
                                if endpoint in self.doc.collections:
                                    response_get = client.get(endpoints[endpoint], headers=self.auth_header)
                                    assert response_get.status_code != 401

    def test_Auth_POST(self):
        """Test for the index."""
        with set_api_name(self.app, self.API_NAME):
            with set_session(self.app, self.session):
                with set_doc(self.app, self.doc):
                    with set_authentication(self.app, True):
                        with self.app.test_client() as client:
                            response_get = client.get("/"+self.API_NAME)
                            endpoints = json.loads(response_get.data.decode('utf-8'))
                            for endpoint in endpoints:
                                if endpoint in self.doc.collections:
                                    response_get = client.post(endpoints[endpoint], headers=self.auth_header, data=json.dumps(dict(foo="bar")))
                                    assert response_get.status_code != 401

    def test_Auth_PUT(self):
        """Test for the index."""
        with set_api_name(self.app, self.API_NAME):
            with set_session(self.app, self.session):
                with set_doc(self.app, self.doc):
                    with set_authentication(self.app, True):
                        with self.app.test_client() as client:
                            response_get = client.get("/"+self.API_NAME)
                            endpoints = json.loads(response_get.data.decode('utf-8'))
                            for endpoint in endpoints:
                                if endpoint in self.doc.collections:
                                    response_get = client.put(endpoints[endpoint], headers=self.auth_header, data=json.dumps(dict(foo="bar")))
                                    assert response_get.status_code != 401

    def test_Auth_DELETE(self):
        """Test for the index."""
        with set_api_name(self.app, self.API_NAME):
            with set_session(self.app, self.session):
                with set_doc(self.app, self.doc):
                    with set_authentication(self.app, True):
                        with self.app.test_client() as client:
                            response_get = client.get("/"+self.API_NAME)
                            endpoints = json.loads(response_get.data.decode('utf-8'))
                            for endpoint in endpoints:
                                if endpoint in self.doc.collections:
                                    response_get = client.delete(endpoints[endpoint], headers=self.auth_header)
                                    assert response_get.status_code != 401


if __name__ == '__main__':
    message = """
    Running tests for authorization. Checking if all responses are in proper order.
    """
    print(message)
    unittest.main()
