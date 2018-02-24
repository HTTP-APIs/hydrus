"""
Pluggable utilities for Hydrus.
===============================
Imports :
contextlib.contextmanager : This function is a decorator that can be used to
define a factory function for with statement context managers, without needing
to create a class or separate __enter__() and __exit__() methods.
Ref- https://docs.python.org/2/library/contextlib.html#contextlib.contextmanager

flask.appcontext_pushed : Signal is sent when an application context is pushed.
The sender is the application.
Ref- http://flask.pocoo.org/docs/0.12/api/#flask.appcontext_pushed
Ref- https://speakerdeck.com/mitsuhiko/advanced-flask-patterns-1

flask.g : Used to attach values to global variables
doc_writer_sample : Sample script used to create Hydra APIDocumentation

hydrus.hydraspec.engine : An SQLalchemy DB engine
sqlalchemy.orm.sessionmaker : Used to create a SQLalchemy Session
sqlalchemy.orm.session.Session : SQLalchemy Session class
Ref- http://docs.sqlalchemy.org/en/latest/orm/session_basics.html

hydrus.hydraspec.doc_writer.HydraDoc : Class for Hydra Documentation
"""

from contextlib import contextmanager
from flask import appcontext_pushed
from flask import g
from hydrus.hydraspec import doc_writer_sample
from hydrus.data.db_models import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from hydrus.hydraspec.doc_writer import HydraDoc


@contextmanager
def set_session(application, DB_SESSION):
    """
    Set the Database Session for the app before it is run in main.py.

    :param application: Flask app object
            <flask.app.Flask>
    :param DB_SESSION: SQLalchemy Session object
            <sqlalchemy.orm.session.Session>
    """
    if not isinstance(DB_SESSION, Session):
        raise TypeError(
            "The API Doc is not of type <sqlalchemy.orm.session.Session>")

    def handler(sender, **kwargs):
        g.dbsession = DB_SESSION
    with appcontext_pushed.connected_to(handler, application):
        yield


def get_session():
    """
    Get the Database Session from g.
    Returns and sets a default Session if not found

    :return session : SQLalchemy Session object
            <sqlalchemy.orm.session.Session>
    """
    session = getattr(g, 'dbsession', None)
    if session is None:
        session = sessionmaker(bind=engine)()
        g.dbsession = session
    return session


@contextmanager
def set_hydrus_server_url(application, server_url):
    """
    Set the server URL for the app (before it is run in main.py).

    :param application: Flask app object
            <flask.app.Flask>
    :param server_url : Server URL
            <str>
    """
    if not isinstance(server_url, str):
        raise TypeError("The server_url is not of type <str>")

    def handler(sender, **kwargs):
        g.hydrus_server_url = server_url
    with appcontext_pushed.connected_to(handler, application):
        yield


def get_hydrus_server_url():
    """
    Get the server URL.
    Returns and sets "http://localhost/" if not found.

    :return hydrus_server_url : Server URL
            <str>
    """
    hydrus_server_url = getattr(g, 'hydrus_server_url', None)
    if hydrus_server_url is None:
        hydrus_server_url = "http://localhost/"
        g.hydrus_server_url = hydrus_server_url
    return hydrus_server_url


@contextmanager
def set_api_name(application, api_name):
    """
    Set the server name or EntryPoint for the app (before it is run in main.py).

    :param application: Flask app object
            <flask.app.Flask>
    :param api_name : API/Server name or EntryPoint
            <str>
    """
    if not isinstance(api_name, str):
        raise TypeError("The api_name is not of type <str>")

    def handler(sender, **kwargs):
        g.api_name = api_name
    with appcontext_pushed.connected_to(handler, application):
        yield


def get_api_name():
    """
    Get the server API name.
    Returns an sets "api" as api_name if not found.

    :return api_name : API/Server name or EntryPoint
            <str>
    """
    api_name = getattr(g, 'api_name', None)
    if api_name is None:
        api_name = "api"
        g.doc = api_name
    return api_name


@contextmanager
def set_doc(application, APIDOC):
    """
    Set the API Documentation for the app (before it is run in main.py).

    :param application: Flask app object
            <flask.app.Flask>
    :param APIDOC : Hydra Documentation object
            <hydrus.hydraspec.doc_writer.HydraDoc>
    """
    if not isinstance(APIDOC, HydraDoc):
        raise TypeError(
            "The API Doc is not of type <hydrus.hydraspec.doc_writer.HydraDoc>")

    def handler(sender, **kwargs):
        g.doc = APIDOC
    with appcontext_pushed.connected_to(handler, application):
        yield


def get_doc():
    """
    Get the server API Documentation.
    Returns and sets doc_writer_sample.api_doc if not found.

    :return apidoc : Hydra Documentation object
            <hydrus.hydraspec.doc_writer.HydraDoc>
    """
    apidoc = getattr(g, 'doc', None)
    if apidoc is None:
        apidoc = doc_writer_sample.api_doc
        g.doc = apidoc
    return apidoc


@contextmanager
def set_authentication(application, authentication):
    """
    Set the whether API needs to be authenticated or not (before it is run in main.py).

    :param application: Flask app object
            <flask.app.Flask>
    :param authentication : Bool. API Auth needed or not
            <bool>
    """
    if not isinstance(authentication, bool):
        raise TypeError("Authentication flag must be of type <bool>")

    def handler(sender, **kwargs):
        g.authentication_ = authentication
    with appcontext_pushed.connected_to(handler, application):
        yield


def get_authentication():
    """
    Check whether API needs to be authenticated or not.
    Return and sets False if not found.

    :return authentication : Bool. API Auth needed or not
            <bool>
    """
    authentication = getattr(g, 'authentication_', None)
    if authentication is None:
        authentication = False
        g.authentication_ = authentication
    return authentication
