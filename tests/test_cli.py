"""Test for checking Cli"""
import unittest
import random
import string
import json
import re
import uuid
from hydrus.app_factory import app_factory
from hydrus.utils import set_session, set_doc, set_api_name
from hydrus.data import doc_parse, crud
from hydra_python_core import doc_maker
from hydra_python_core.doc_writer import HydraLink
from hydrus.samples import doc_writer_sample
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from hydrus.data.db_models import Base
import click
from click.testing import CliRunner
from cli import startserver


def gen_dummy_object(class_, doc):
    """Create a dummy object based on the definitions in the API Doc."""
    object_ = {
        "@type": class_
    }
    if class_ in doc.parsed_classes:
        for prop in doc.parsed_classes[class_]["class"].supportedProperty:
            if isinstance(prop.prop, HydraLink):
                continue
            if "vocab:" in prop.prop:
                prop_class = prop.prop.replace("vocab:", "")
                object_[prop.title] = gen_dummy_object(prop_class, doc)
            else:
                object_[prop.title] = ''.join(random.choice(
                    string.ascii_uppercase + string.digits) for _ in range(6))
        return object_


class CliTests(unittest.TestCase):
    """Test Class for the Cli."""

    @classmethod
    def setUpClass(self):
        """Database setup before the tests."""
        print("Creating a temporary database...")
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        session = scoped_session(sessionmaker(bind=engine))

        self.session = session
        self.API_NAME = "demoapi"
        self.HYDRUS_SERVER_URL = "http://hydrus.com/"

        self.app = app_factory(self.API_NAME)
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

        print("Setting up Hydrus utilities... ")
        self.api_name_util = set_api_name(self.app, self.API_NAME)
        self.session_util = set_session(self.app, self.session)
        self.doc_util = set_doc(self.app, self.doc)
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
            if class_ not in self.doc.collections:
                dummy_obj = gen_dummy_object(class_, self.doc)
                crud.insert(
                    dummy_obj,
                    id_=str(
                        uuid.uuid4()),
                    session=self.session)

    def test_startserver(self):
        runner = CliRunner()
        # Starting server with valid parameters
        result = runner.invoke(startserver,
                               ["--adduser", "--api", "--no-auth", "--dburl",
                                "--hydradoc", "--port", "--no-token", "--serverurl",
                                "serve"])
        result.exit_code != 0

        # Starting server with invalid parameters

        result = runner.invoke(startserver,
                               ["--adduser", "sqlite://not-valid", "http://localhost",
                                "--port", "serve"])
        assert result.exit_code == 2


if __name__ == '__main__':
    message = """
    Running tests for the cli
    """
    unittest.main()
