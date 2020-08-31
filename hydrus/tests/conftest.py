import random
import string
import uuid
from base64 import b64encode

import pytest
from hydra_python_core import doc_maker
from hydra_python_core.doc_writer import DocUrl, HydraLink
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from hydrus.app_factory import app_factory
from hydrus.data import crud, doc_parse
from hydrus.data.db_models import Base, create_database_tables
from hydrus.data.user import add_user
from hydrus.helpers import get_path_from_type
from hydrus.samples import doc_writer_sample, hydra_doc_sample
from hydrus.socketio_factory import create_socket
from hydrus.utils import (get_api_name, get_session, set_api_name,
                          set_authentication, set_doc, set_page_size,
                          set_session, set_token)


def get_doc_classes_and_properties(doc):
    """
    Extract classes and properties from a given HydraDoc object

    :param doc: HydraDoc object whose classes and properties have to extracted
    :type doc: HydraDoc
    :return: classes and properties in the HydraDoc object in a tuple
    :rtype: tuple(list, set)
    """
    test_classes = doc_parse.get_classes(doc)
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
    expanded_base_url = DocUrl.doc_url
    for class_path in doc.collections:
        if class_title == doc.collections[class_path]["collection"].name:
            members = list()
            manages_class_titles = list()
            collection_manages = doc.collections[class_title]["collection"].manages
            if type(collection_manages) is dict:
                # only one manages block
                manages_class = collection_manages['object'].split(expanded_base_url)[1]
                manages_class_titles.append(manages_class)
            elif type(collection_manages) is list:
                # multiple manages block
                for manages_block in collection_manages:
                    manages_class = collection_manages['object'].split(expanded_base_url)[1]
                    manages_class_titles.append(manages_class)
            for _ in range(3):
                member_class = random.choice(manages_class_titles)
                member = gen_dummy_object(member_class, doc)
                member_id = crud.insert(object_=member,
                                        session=get_session(),
                                        collection=False)
                member_class_path = get_path_from_type(member_class)
                member_api_path = f'/{get_api_name()}/{member_class_path}/{member_id}'
                members.append({
                    "@id": member_api_path,
                    "@type": member_class,
                })
            object_['members'] = members
            return object_
    for class_path in doc.parsed_classes:
        if class_title == doc.parsed_classes[class_path]["class"].title:
            for prop in doc.parsed_classes[class_path]["class"].supportedProperty:
                if prop.write is False:
                    continue
                if isinstance(prop.prop, HydraLink):
                    object_[prop.title] = ''.join(random.choice(
                        string.ascii_uppercase + string.digits) for _ in range(6))
                    pass
                elif expanded_base_url in prop.prop:
                    prop_class = prop.prop.split(expanded_base_url)[1]
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
        'HYDRUS_SERVER_URL': 'http://hydrus.com/',
        'PAGE_SIZE': 1
    }


@pytest.fixture(scope='module', name='doc')
def test_doc(constants):
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
def session(engine):
    """
    Initialize a flask scoped session binded with a database
    """
    session = scoped_session(sessionmaker(bind=engine))
    yield session
    session.close()


@pytest.fixture(scope='module')
def engine():
    """
    Initialize a sqlalchemy engine binded with a database
    """
    engine = create_engine('sqlite:///:memory:')
    return engine


@pytest.fixture(scope='module')
def init_db_for_auth_tests(doc, session, engine):
    """
    Initialize the database by adding the classes and properties of
    test HydraDoc object and adding a user to the database
    """
    test_classes, test_properties = get_doc_classes_and_properties(doc)
    Base.metadata.create_all(engine)
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


@pytest.fixture(scope='module')
def put_allowed_class_names(doc):
    """
    Get the names of all the parsed classes endpoints in a given HydraDoc object
    """

    allowed_classes = list()
    for parsed_class in doc.parsed_classes.values():
        for operation in parsed_class['class'].supportedOperation:
            if operation.method == 'PUT':
                allowed_classes.append(parsed_class['class'].title)
    return allowed_classes


@pytest.fixture(scope='module', name='test_client')
def test_client_for_auth_tests(constants, session, doc, init_db_for_auth_tests, app):
    """
    Get a test flask app for testing
    """
    API_NAME = constants['API_NAME']
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
def drone_doc_parsed_classes(drone_doc):
    return [drone_doc.parsed_classes[i]['class'].title for i in drone_doc.parsed_classes]


@pytest.fixture(scope='module')
def init_db_for_crud_tests(drone_doc, session, engine):
    """
    Initialize the database by adding the classes and properties of
    Drone Api test HydraDoc object.
    """
    test_classes, test_properties = get_doc_classes_and_properties(drone_doc)
    create_database_tables(test_classes)
    Base.metadata.create_all(engine)


@pytest.fixture(scope='module')
def app(constants):
    """
    Get a test flask app for testing in test
    """
    API_NAME = constants['API_NAME']
    app = app_factory(API_NAME)
    return app


@pytest.fixture(scope='module', name='test_app_client')
def test_client_for_app_tests(app, session, constants, doc):
    API_NAME = constants['API_NAME']
    PAGE_SIZE = constants['PAGE_SIZE']
    with set_api_name(app, API_NAME):
        with set_session(app, session):
            with set_doc(app, doc):
                with set_page_size(app, PAGE_SIZE):
                    testing_client = app.test_client()
                    # Establish an application context before running the tests.
                    ctx = app.app_context()
                    ctx.push()
                    yield testing_client
                    ctx.pop()


@pytest.fixture()
def init_db_for_app_tests(doc, constants, session, add_doc_classes_and_properties_to_db):
    """
    Initalze the database for testing app in
    tests/functional/test_app.py.
    """
    for class_ in doc.parsed_classes:
        class_title = doc.parsed_classes[class_]['class'].title
        dummy_obj = gen_dummy_object(class_title, doc)
        crud.insert(dummy_obj, id_=str(uuid.uuid4()), session=session)
        # If it's a collection class then add an extra object so
        # we can test pagination thoroughly.
        if class_ in doc.collections:
            crud.insert(dummy_obj, id_=str(uuid.uuid4()), session=session)


@pytest.fixture()
def init_db_for_socket_tests(doc, add_doc_classes_and_properties_to_db, session):
    """
    Initalze the database for testing app in
    tests/functional/test_socket.py.
    """
    for class_ in doc.parsed_classes:
        class_title = doc.parsed_classes[class_]["class"].title
        dummy_obj = gen_dummy_object(class_title, doc)
        crud.insert(dummy_obj, id_=str(uuid.uuid4()), session=session)
        # If it's a collection class then add an extra object so
        # we can test pagination thoroughly.
        if class_ in doc.collections:
            crud.insert(dummy_obj, id_=str(uuid.uuid4()), session=session)
    # Add two dummy modification records
    crud.insert_modification_record(method="POST", resource_url="", session=session)
    crud.insert_modification_record(method="DELETE", resource_url="", session=session)


@pytest.fixture(scope='module')
def socketio(app, session):
    socket = create_socket(app, session)
    return socket


@pytest.fixture(scope='module')
def socketio_client(app, session, constants, doc, socketio):
    API_NAME = constants['API_NAME']
    PAGE_SIZE = constants['PAGE_SIZE']
    with set_api_name(app, API_NAME):
        with set_session(app, session):
            with set_doc(app, doc):
                with set_page_size(app, PAGE_SIZE):
                    socketio_client = socketio.test_client(app, namespace='/sync')
                    return socketio_client


@pytest.fixture(scope='module')
def add_doc_classes_and_properties_to_db(doc, session, engine):
    """
    Add the doc classes and properties to database
    for testing in /functional/test_app.py and
    /functional/test_socket.py
    """
    test_classes, test_properties = get_doc_classes_and_properties(doc)
    # temporarily add manages block explicitly to collection-classes
    # until appropriate changes take place in hydra-python-core library
    manages = {
        "object": "vocab:dummyClass",
        "property": "rdf:type"
    }
    for class_ in test_classes:
        if "Collection" in class_['@id']:
            class_['manages'] = manages

    try:
        create_database_tables(test_classes)
    except Exception:
        # catch error when the tables have been already defined.
        # happens when /test_socket.py is run after /test_app.py
        # in the same session
        # in that case, no need to create the tables again on the
        # same sqlalchemy.ext.declarative.declarative_base instance
        pass
    Base.metadata.create_all(engine)
