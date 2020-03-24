import random
import string
from base64 import b64encode

import pytest
from hydra_python_core import doc_maker
from hydra_python_core.doc_writer import HydraLink
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from hydrus.app_factory import app_factory
from hydrus.data import doc_parse
from hydrus.data.db_models import Base
from hydrus.data.user import add_user
from hydrus.samples import doc_writer_sample, hydra_doc_sample
from hydrus.utils import (set_api_name, set_authentication, set_doc,
                          set_session, set_token)


def get_doc_classes_and_properties(doc):
    """
    Extract classes and properties from a given HydraDoc object 

    :param doc: HydraDoc object whose classes and properties have to extracted
    :type doc: HydraDoc
    :return: classes and properties in the HydraDoc object in a tuple
    :rtype: tuple(list, set)
    """
    test_classes = doc_parse.get_classes(doc.generate())
    test_properties = doc_parse.get_all_properties(test_classes)
    return (test_classes, test_properties)


def gen_dummy_object(class_title, doc):
    """
    Create a dummy object based on the definitions in the API Doc.
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


@pytest.fixture(scope='module')
def constants():
    """
    Constant values to be used in all tests
    """
    return {
        'API_NAME': 'demoapi',
        'HYDRUS_SERVER_URL': 'http://hydrus.com/'
    }


@pytest.fixture(scope='module', name='doc')
def auth_test_doc(constants):
    """
    Generate a test HydraDoc object from a Api Documentation
    """
    HYDRUS_SERVER_URL = constants['HYDRUS_SERVER_URL']
    API_NAME = constants['API_NAME']

    doc = doc_maker.create_doc(doc_writer_sample.api_doc.generate(),
                               HYDRUS_SERVER_URL,
                               API_NAME)
    return doc


@pytest.fixture(scope='module')
def session():
    """
    Initialize a flask scoped session binded with a database
    """
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    session = scoped_session(sessionmaker(bind=engine))
    yield session
    session.close()


@pytest.fixture(scope='module')
def init_db_for_auth_tests(doc, session):
    """
    Initialize the database by adding the classes and properties of
    test HydraDoc object and adding a user to the database
    """
    test_classes, test_properties = get_doc_classes_and_properties(doc)
    doc_parse.insert_classes(test_classes, session)
    doc_parse.insert_properties(test_properties, session)
    add_user(1, 'test', session)


@pytest.fixture()
def headers_with_wrong_id():
    """
    Get headers for wrong id and correct user paraphrase in credentials
    """
    credentials_with_wrong_id = b64encode(b"2:test").decode("ascii")
    headers = {"X-Authentication": "",
               "Authorization": f"Basic {credentials_with_wrong_id}"}
    return headers


@pytest.fixture()
def headers_with_wrong_pass():
    """
    Get headers for wrong user paraphrase and correct user id in credentials
    """
    credentials_with_wrong_pass = b64encode(b"1:test2").decode("ascii")
    headers = {"X-Authentication": "",
               "Authorization": f"Basic {credentials_with_wrong_pass}"}
    return headers


@pytest.fixture()
def headers_with_correct_pass_and_id():
    """
    Get headers for correct paraphrase and id in credentials
    """
    correct_credentials = b64encode(b"1:test").decode("ascii")
    headers = {"X-Authentication": "",
               "Authorization": f"Basic {correct_credentials}"}
    return headers


@pytest.fixture(scope='module')
def collection_names(doc):
    """
    Get the names of all the collection endpoints in a given HydraDoc object
    """
    return [collection_object['collection'].name
            for collection_object in doc.collections.values()]


@pytest.fixture(scope='module', name='test_client')
def test_client_for_auth_tests(constants, session, doc, init_db_for_auth_tests):
    """
    Get a test flask app for testing
    """
    API_NAME = constants['API_NAME']
    app = app_factory(API_NAME)
    with set_authentication(app, True):
        with set_token(app, False):
            with set_api_name(app, API_NAME):
                with set_doc(app, doc):
                    with set_session(app, session):
                        testing_client = app.test_client()
                        # Establish an application context before running the tests.
                        ctx = app.app_context()
                        ctx.push()
                        yield testing_client
                        ctx.pop()


@pytest.fixture(scope='module')
def drone_doc(constants):
    API_NAME = constants['API_NAME']
    HYDRUS_SERVER_URL = constants['HYDRUS_SERVER_URL']
    doc = doc_maker.create_doc(hydra_doc_sample.doc, HYDRUS_SERVER_URL, API_NAME)
    return doc


@pytest.fixture(scope='module')
def drone_doc_collection_classes(drone_doc):
    return [drone_doc.collections[i]['collection'].class_.title for i in drone_doc.collections]


@pytest.fixture(scope='module')
def init_db_for_crud_tests(drone_doc, session):
    """
    Initialize the database by adding the classes and properties of
    Drone Api test HydraDoc object.
    """
    test_classes, test_properties = get_doc_classes_and_properties(drone_doc)
    doc_parse.insert_classes(test_classes, session)
    doc_parse.insert_properties(test_properties, session)
