# Pluggable utilities for hydrus.
# ===============================
# This module is for Web server-related utilities. For data-related
#  utilities use `data.helpers`

# Imports :

# contextlib module used

# contextlib.contextmanager : This function is a decorator that can be used to
#                             define a factory function for with statement context 
#                             managers, without needing to create a class or separate 
#                             __enter__() and __exit__() methods.
# Ref- https://docs.python.org/2/library/contextlib.html#contextlib.contextmanager
from contextlib import contextmanager

# sqlalchemy module used

# sqlalchemy.orm.sessionmaker    : Used to create a SQLalchemy Session
# sqlalchemy.orm.scoped_session  : Used to create a SQLalchemy Scoped_session
# sqlalchemy.orm.session.Session : SQLalchemy Session class
# Ref- http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.session import Session

# flask module used

# flask.g                 : Used to attach values to global variables
# flask.Response          :
# flask.jsonify           :
# flask.appcontext_pushed :
# flask.app.Flask         :
# flask.appcontext_pushed : Signal is sent when an application context is pushed. 
#                           The sender is the application.
# Ref- http://flask.pocoo.org/docs/0.12/api/#flask.appcontext_pushed
# Ref- https://speakerdeck.com/mitsuhiko/advanced-flask-patterns-1
from flask import g, Response, jsonify , appcontext_pushed , Flask

# typing 
# 

from typing import Any, Iterator , Dict, List

# hrdyus modules

# hydrus.samples.doc_writer_sample        : Sample script used to create Hydra APIDocumentation
# hydrus.data.db_models.engine            : An SQLalchemy DB engine
# hydra_python_core.doc_writer.HydraDoc   : Class for Hydra Documentation
# hydra_python_core.doc_writer.HydraError : Class for Hydra Error
from hydrus.samples import doc_writer_sample
from hydrus.data.db_models import engine
from hydra_python_core.doc_writer import HydraDoc , HydraError

def error(value,data_type,error_msg):
    if not isinstance(value,data_type):
        raise TypeError(error_msg)
    
def error_2(value_1 , data_type_1 , value_2 , data_type_2 , error_msg):
    if not isinstance(value_1, data_type_1) and not isinstance(value_1, data_type_2):
        raise TypeError(error_msg)

def try_except_block(value_1,value_2,value_3,value_4):
    try:
        value_1 = getattr(g, value_2)
    except AttributeError:
        value_1 = value_3
        value_4 = value_1
    return value_1
    
def appcontext_pushed_function():
    with appcontext_pushed.connected_to(handler, application):
        yield

@contextmanager
def set_authentication(application: Flask, authentication: bool) -> Iterator:
    # set_authentication : 
    #                     Set the whether API needs to be authenticated or not (before it is run in main.py).

    # :param application: Flask app object
    #         <flask.app.Flask>
    # :param authentication : Bool. API Auth needed or not
    #         <bool>

    # Raises:
    #        TypeError: If `authentication` is not a boolean value.

    error(authentication, bool,"Authentication flag must be of type <bool>")

    def handler(sender: Flask, **kwargs: Any) -> None:
        g.authentication_ = authentication
    
    appcontext_pushed_function()


def get_authentication() -> bool:

    # Check whether API needs to be authenticated or not.
    # Return and sets False if not found.
    # :return authentication : Bool. API Auth needed or not
    #         <bool>

    return try_except_block(authentication,"authentication_",False,g.authentication_)


@contextmanager
def set_api_name(application: Flask, api_name: str) -> Iterator:

    # Set the server name or EntryPoint for the app (before it is run in main.py).
    # :param application: Flask app object
    #         <flask.app.Flask>
    # :param api_name : API/Server name or EntryPoint
    #         <str>

    # Raises:
    #     TypeError: If `api_name` is not a string.


    error(api_name, str,"The api_name is not of type <str>")

    def handler(sender: Flask, **kwargs: Any) -> None:
        g.api_name = api_name

    appcontext_pushed_function()


def get_api_name() -> str:

    # Get the server API name.
    # Returns an sets "api" as api_name if not found.
    # :return api_name : API/Server name or EntryPoint
    #         <str>

    return try_except_block(api_name,"api_name","api",g.api_name)


@contextmanager
def set_page_size(application: Flask, page_size: int) -> Iterator:

    # Set the page_size of a page view.
    # :param application: Flask app object
    #         <flask.app.Flask>
    # :param page_size : Number of maximum elements a page can contain
    #         <int>

    # Raises:
    #     TypeError: If `page_size` is not an int.


    error(page_size, int , "The page_size is not of type <int>")

    def handler(sender: Flask, **kwargs: Any) -> None:
        g.page_size = page_size

    appcontext_pushed_function()


def get_page_size() -> int:

    # Get the page_size of a page-view.
    # :return page_size : Number of maximum elements a page view can contain.
    #         <int>

    return try_except_block(page_size,"page_size",10,g.page_size)


@contextmanager
def set_pagination(application: Flask, paginate: bool) -> Iterator:

    # Enable or disable pagination.
    # :param application: Flask app object
    #         <flask.app.Flask>
    # :param paginate : Pagination enabled or not
    #         <bool>

    # Raises:
    #     TypeError: If `paginate` is not a bool.


    error(paginate, bool,"The CLI argument 'pagination' is not of type <bool>")
    
    def handler(sender: Flask, **kwargs: Any) -> None:
        g.paginate = paginate

    appcontext_pushed_function()


def get_pagination() -> bool:

    # Get the pagination status(Enable/Disable).
    # :return paginate : Pagination enabled or not
    #         <bool>

    return try_except_block(paginate,"paginate",True,g.paginate)


@contextmanager
def set_doc(application: Flask, APIDOC: HydraDoc) -> Iterator:

    # Set the API Documentation for the app (before it is run in main.py).
    # :param application: Flask app object
    #         <flask.app.Flask>
    # :param APIDOC : Hydra Documentation object
    #         <hydra_python_core.doc_writer.HydraDoc>

    # Raises:
    #     TypeError: If `APIDOC` is not an instance of `HydraDoc`.


    error(APIDOC, HydraDoc,"The API Doc is not of type <hydra_python_core.doc_writer.HydraDoc>")

    def handler(sender: Flask, **kwargs: Any) -> None:
        g.doc = APIDOC

    appcontext_pushed_function()


@contextmanager
def set_token(application: Flask, token: bool) -> Iterator:
    # Set whether API needs to implement token based authentication.

    # Raises:
    #     TypeError: If `token` is not a boolean value.

    error(token, bool,"Token flag must be of type <bool>")

    def handler(sender: Flask, **kwargs: Any) -> None:
        g.token_ = token

    appcontext_pushed_function()


def get_doc() -> HydraDoc:

    # Get the server API Documentation.
    # Returns and sets doc_writer_sample.api_doc if not found.
    # :return apidoc : Hydra Documentation object
    #         <hydra_python_core.doc_writer.HydraDoc>

    return try_except_block(apidoc,"doc",g.doc,doc_writer_sample.api_doc)


def get_token() -> bool:
    # Check wether API needs to be authenticated or not.
    return try_except_block(token,"token_",False,g.token_)


@contextmanager
def set_hydrus_server_url(application: Flask, server_url: str) -> Iterator:

    # Set the server URL for the app (before it is run in main.py).
    # :param application: Flask app object
    #         <flask.app.Flask>
    # :param server_url : Server URL
    #         <str>

    # Raises:
    #     TypeError: If the `server_url` is not a string.

    error(server_url, str,"The server_url is not of type <str>")

    def handler(sender: Flask, **kwargs: Any) -> None:
        g.hydrus_server_url = server_url

    appcontext_pushed_function()


def get_hydrus_server_url() -> str:

    # Get the server URL.
    # Returns and sets "http://localhost/" if not found.
    # :return hydrus_server_url : Server URL
    #         <str>

    return try_except_block(hydrus_server_url,"hydrus_server_url","http://localhost/",g.hydrus_server_url)


@contextmanager
def set_session(application: Flask, DB_SESSION: scoped_session) -> Iterator:

    # Set the Database Session for the app before it is run in main.py.
    # :param application: Flask app object
    #         <flask.app.Flask>
    # :param DB_SESSION: SQLalchemy Session object
    #         <sqlalchemy.orm.session.Session>

    # Raises:
    #     TypeError: If `DB_SESSION` is not an instance of `scoped_session` or `Session`.


    error_2(DB_SESSION, scoped_session,DB_SESSION, Session,"The API Doc is not of type <sqlalchemy.orm.session.Session> or\n<sqlalchemy.orm.scoping.scoped_session>")

    def handler(sender: Flask, **kwargs: Any) -> None:
        g.dbsession = DB_SESSION

    appcontext_pushed_function()


def get_session() -> scoped_session:

    # Get the Database Session from g.
    # Returns and sets a default Session if not found
    # :return session : SQLalchemy Session object
    #         <sqlalchemy.orm.scoped_session>

    return try_except_block(session,"dbsession",scoped_session(sessionmaker(bind=engine)),g.dbsession)


def set_response_headers(resp: Response,ct: str = "application/ld+json",headers: List[Dict[str, Any]]=[],status_code: int = 200,) -> Response:

    # Set the response headers.
    # :param resp: Response.
    # :param ct: Content-type default "application/ld+json".
    # :param headers: List of objects.
    # :param status_code: status code default 200.
    # :return: Response with headers.

    resp.status_code = status_code
    for header in headers:
        resp.headers[list(header.keys())[0]] = header[list(header.keys())[0]]
    resp.headers["Content-type"] = ct
    link = "http://www.w3.org/ns/hydra/core#apiDocumentation"
    vocab_route = get_doc().doc_name
    link_header = (
        f'<{get_hydrus_server_url()}{get_api_name()}/{vocab_route}>; rel="{link}"'
    )
    resp.headers["Link"] = link_header
    return resp


def error_response(error: HydraError) -> Response:

    # Generate the response if there is an error while performing any operation

    # :param error: HydraError object which will help in generating response
    # :type error: HydraError
    # :return: Error response with appropriate status code
    # :rtype: Response

    return set_response_headers(jsonify(error.generate()), status_code=error.code)
