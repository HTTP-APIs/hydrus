"""Pluggable utilities for Hydrus."""

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
    """Set the database session for the app. Must be of type <hydrus.hydraspec.doc_writer.HydraDoc>."""
    if not isinstance(DB_SESSION, Session):
        raise TypeError("The API Doc is not of type <sqlalchemy.orm.session.Session>")

    def handler(sender, **kwargs):
        g.dbsession = DB_SESSION
    with appcontext_pushed.connected_to(handler, application):
        yield


@contextmanager
def set_hydrus_server_url(application, server_url):
    """Set the server URL for the app. Must be of type <str>."""
    if not isinstance(server_url, str):
        raise TypeError("The server_url is not of type <str>")

    def handler(sender, **kwargs):
        g.hydrus_server_url = server_url
    with appcontext_pushed.connected_to(handler, application):
        yield


@contextmanager
def set_api_name(application, api_name):
    """Set the server name or EntryPoint for the app. Must be of type <str>."""
    if not isinstance(api_name, str):
        raise TypeError("The api_name is not of type <str>")

    def handler(sender, **kwargs):
        g.api_name = api_name
    with appcontext_pushed.connected_to(handler, application):
        yield


@contextmanager
def set_doc(application, APIDOC):
    """Set the API Documentation for the app. Must be of type <hydrus.hydraspec.doc_writer.HydraDoc>."""
    if not isinstance(APIDOC, HydraDoc):
        raise TypeError("The API Doc is not of type <hydrus.hydraspec.doc_writer.HydraDoc>")

    def handler(sender, **kwargs):
        g.doc = APIDOC
    with appcontext_pushed.connected_to(handler, application):
        yield


def get_doc():
    """Get the server API Documentation."""
    apidoc = getattr(g, 'doc', None)
    if apidoc is None:
        apidoc = doc_writer_sample.api_doc
        g.doc = apidoc
    return apidoc


def get_api_name():
    """Get the server API name."""
    api_name = getattr(g, 'api_name', None)
    if api_name is None:
        api_name = "api"
        g.doc = api_name
    return api_name


def get_hydrus_server_url():
    """Get the server URL."""
    hydrus_server_url = getattr(g, 'hydrus_server_url', None)
    if hydrus_server_url is None:
        hydrus_server_url = "http://localhost/"
        g.hydrus_server_url = hydrus_server_url
    return hydrus_server_url


def get_session():
    """Get the Database Session for the server."""
    session = getattr(g, 'dbsession', None)
    if session is None:
        session = sessionmaker(bind=engine)()
        g.dbsession = session
    return session
