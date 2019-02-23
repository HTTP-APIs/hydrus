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
hydra_python_core.engine : An SQLalchemy DB engine
sqlalchemy.orm.sessionmaker : Used to create a SQLalchemy Session
sqlalchemy.orm.session.Session : SQLalchemy Session class
Ref- http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
hydra_python_core.doc_writer.HydraDoc : Class for Hydra Documentation
"""  # nopep8

from contextlib import contextmanager
from flask import appcontext_pushed
from flask import g
from hydrus.samples import doc_writer_sample
from hydrus.data.db_models import engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session
from hydra_python_core.doc_writer import HydraDoc
from flask.app import Flask
from typing import Any, Iterator


@contextmanager
def set_authentication(application: Flask, authentication: bool) -> Iterator:
    """
    Set the whether API needs to be authenticated or not (before it is run in main.py).

    :param application: Flask app object
            <flask.app.Flask>
    :param authentication : Bool. API Auth needed or not
            <bool>


    Raises:
        TypeError: If `authentication` is not a boolean value.

    """
    if not isinstance(authentication, bool):
        raise TypeError("Authentication flag must be of type <bool>")

    def handler(sender: Flask, **kwargs: Any) -> None:
        g.authentication_ = authentication
    with appcontext_pushed.connected_to(handler, application):
        yield


def get_authentication() -> bool:
    """
    Check whether API needs to be authenticated or not.
    Return and sets False if not found.
    :return authentication : Bool. API Auth needed or not
            <bool>
    """
    try:
        authentication = getattr(g, 'authentication_')
    except AttributeError:
        authentication = False
        g.authentication_ = authentication
    return authentication


@contextmanager
def set_api_name(application: Flask, api_name: str) -> Iterator:
    """
    Set the server name or EntryPoint for the app (before it is run in main.py).
    :param application: Flask app object
            <flask.app.Flask>
    :param api_name : API/Server name or EntryPoint
            <str>

    Raises:
        TypeError: If `api_name` is not a string.

    """
    if not isinstance(api_name, str):
        raise TypeError("The api_name is not of type <str>")

    def handler(sender: Flask, **kwargs: Any) -> None:
        g.api_name = api_name
    with appcontext_pushed.connected_to(handler, application):
        yield


def get_api_name() -> str:
    """
    Get the server API name.
    Returns an sets "api" as api_name if not found.
    :return api_name : API/Server name or EntryPoint
            <str>
    """
    try:
        api_name = getattr(g, 'api_name')
    except AttributeError:
        api_name = "api"
        g.doc = api_name
    return api_name


@contextmanager
def set_doc(application: Flask, APIDOC: HydraDoc) -> Iterator:
    """
    Set the API Documentation for the app (before it is run in main.py).
    :param application: Flask app object
            <flask.app.Flask>
    :param APIDOC : Hydra Documentation object
            <hydra_python_core.doc_writer.HydraDoc>

    Raises:
        TypeError: If `APIDOC` is not an instance of `HydraDoc`.

    """
    if not isinstance(APIDOC, HydraDoc):
        raise TypeError(
            "The API Doc is not of type <hydra_python_core.doc_writer.HydraDoc>")

    def handler(sender: Flask, **kwargs: Any) -> None:
        g.doc = APIDOC
    with appcontext_pushed.connected_to(handler, application):
        yield


@contextmanager
def set_token(application: Flask, token: bool) -> Iterator:
    """Set whether API needs to implement token based authentication.

    Raises:
        TypeError: If `token` is not a boolean value.

    """
    if not isinstance(token, bool):
        raise TypeError("Token flag must be of type <bool>")

    def handler(sender: Flask, **kwargs: Any) -> None:
        g.token_ = token
    with appcontext_pushed.connected_to(handler, application):
        yield


def get_doc() -> HydraDoc:
    """
    Get the server API Documentation.
    Returns and sets doc_writer_sample.api_doc if not found.
    :return apidoc : Hydra Documentation object
            <hydra_python_core.doc_writer.HydraDoc>
    """
    try:
        apidoc = getattr(g, 'doc')
    except AttributeError:
        g.doc = apidoc = doc_writer_sample.api_doc
    return apidoc


def get_token() -> bool:
    """Check wether API needs to be authenticated or not."""
    try:
        token = getattr(g, 'token_')
    except AttributeError:
        token = False
        g.token_ = token
    return token


@contextmanager
def set_hydrus_server_url(application: Flask, server_url: str) -> Iterator:
    """
    Set the server URL for the app (before it is run in main.py).
    :param application: Flask app object
            <flask.app.Flask>
    :param server_url : Server URL
            <str>

    Raises:
        TypeError: If the `server_url` is not a string.

    """
    if not isinstance(server_url, str):
        raise TypeError("The server_url is not of type <str>")

    def handler(sender: Flask, **kwargs: Any) -> None:
        g.hydrus_server_url = server_url
    with appcontext_pushed.connected_to(handler, application):
        yield


def get_hydrus_server_url() -> str:
    """
    Get the server URL.
    Returns and sets "http://localhost/" if not found.
    :return hydrus_server_url : Server URL
            <str>
    """
    try:
        hydrus_server_url = getattr(g, 'hydrus_server_url')
    except AttributeError:
        hydrus_server_url = "http://localhost/"
        g.hydrus_server_url = hydrus_server_url
    return hydrus_server_url


@contextmanager
def set_session(application: Flask, DB_SESSION: scoped_session) -> Iterator:
    """
    Set the Database Session for the app before it is run in main.py.
    :param application: Flask app object
            <flask.app.Flask>
    :param DB_SESSION: SQLalchemy Session object
            <sqlalchemy.orm.session.Session>

    Raises:
        TypeError: If `DB_SESSION` is not an instance of `scoped_session` or `Session`.

    """
    if not isinstance(DB_SESSION, scoped_session) and not isinstance(
            DB_SESSION, Session):
        raise TypeError(
            "The API Doc is not of type <sqlalchemy.orm.session.Session> or"
            " <sqlalchemy.orm.scoping.scoped_session>")

    def handler(sender: Flask, **kwargs: Any) -> None:
        g.dbsession = DB_SESSION
    with appcontext_pushed.connected_to(handler, application):
        yield


def get_session() -> scoped_session:
    """
    Get the Database Session from g.
    Returns and sets a default Session if not found
    :return session : SQLalchemy Session object
            <sqlalchemy.orm.scoped_session>
    """
    try:
        session = getattr(g, 'dbsession')
    except AttributeError:
        session = scoped_session(sessionmaker(bind=engine))
        g.dbsession = session
    return session
