from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from hydrus.app import app_factory, checkEndpoint, getType
from hydrus.utils import (set_session, set_doc, set_hydrus_server_url,
                          set_api_name, set_authentication, get_session,
                          get_doc)
from hydrus.data import doc_parse, crud
from hydrus.hydraspec import doc_maker
from hydrus.hydraspec.doc_writer import HydraDoc
from hydrus.data.db_models import Base
from hydrus.data.user import add_user
from gevent.wsgi import WSGIServer
import json
import click
from flask import Flask
from typing import IO, Any, Dict, Tuple


@click.group()
def cli():
    pass


@cli.command()
@click.option("--adduser", "-u", default=tuple([1, "test"]),
              help="Adds a new user to the API.", nargs=2, type=(int, str))
@click.option("--api", "-a", default="serverapi",
              help="The API name.", type=str)
@click.option("--auth/--no-auth", default=True,
              help="Set authentication to True or False.")
@click.option("--dburl", default="sqlite:///:memory:",
              help="Set database url", type=str)
@click.option("--hydradoc", "-d", default="doc.jsonld",
              help="Location to HydraDocumentation (JSON-LD) of server.",
              type=click.File('r'))
@click.option("--port", "-p", default=8080,
              help="The port the app is hosted at.",
              type=int)
@click.option("--serverurl", default="http://localhost",
              help="Set server url", type=str)
def serve(adduser: Tuple[int, str], api: str, auth: bool, dburl: str,
          hydradoc: IO[Any], port: int, serverurl: str):
    """
    Starts the server : "hydrus serve --help" 
    """
    (app, apidoc, HYDRUS_SERVER_URL, API_NAME, session) = setup_app(
        adduser, api, auth, dburl, hydradoc, port, serverurl)
    click.echo("Starting the application")
    with set_authentication(app, auth):
        # Use authentication for all :equests
        with set_api_name(app, api):
            # Set the API Documentation
            with set_doc(app, apidoc):
                # Set HYDRUS_SERVER_URL
                with set_hydrus_server_url(app, HYDRUS_SERVER_URL):
                    # Set the Database session
                    with set_session(app, session):
                        # Start the Hydrus app
                        http_server = WSGIServer(('', port), app)
                        click.echo("Server running at:")
                        click.echo(HYDRUS_SERVER_URL + API_NAME)
                        try:
                            http_server.serve_forever()
                        except KeyboardInterrupt:
                            pass


@cli.command()
@click.option("--datafile", "-d", required=True,
              help="Location to the file containing ITEMS data.",
              type=click.File('r'))
@click.option("--hydradoc", "-h", required=True,
              help="Location to HydraDocumentation (JSON-LD).",
              type=click.File('r'))
@click.option("--database", required=True,
              help="Set database url",
              type=str)
def additems(datafile: IO[Any], hydradoc: IO[Any], database: str):
    """
    Add Items to Collection : hydrus additems --help
    """
    adduser = tuple([1, "test"])
    api = "serverapi"
    auth = True
    dburl = database
    port = 8080
    serverurl = "http://localhost"
    (app, apidoc, HYDRUS_SERVER_URL, API_NAME, session) = setup_app(
        adduser, api, auth, dburl, hydradoc, port, serverurl)
    with set_authentication(app, auth):
        # Use authentication for all :equests
        with set_api_name(app, api):
            # Set the API Documentation
            with set_doc(app, apidoc):
                # Set HYDRUS_SERVER_URL
                with set_hydrus_server_url(app, HYDRUS_SERVER_URL):
                    # Set the Database session
                    with set_session(app, session):
                        with app.app_context():
                            parse_json(datafile)


def parse_json(datafile: IO[Any]) -> None:
    """
        Method that parses a datafile containing json 
        data of the format [{"Prop1":"Value1","Prop2":"Value2","@type":"dummyClass"}
        ,{"Prop1":"Value1","Prop2":"Value2","@type":"dummyClass"}]

        :param datafile: expects a file object
        :return : None

    """
    data_ = json.loads(datafile.read())
    for object_ in data_:
        type_ = object_.get("@type", None)
        if (type_):
            success = add_to_collection(object_, type_ + "Collection")
            if (success is False):
                return None
        else:
            print("Data is invalid")
            return None


def setup_app(adduser: Tuple[int, str], api: str, auth: bool, dburl: str,
              hydradoc: IO[Any], port: int,
              serverurl: str) -> Tuple[Flask, HydraDoc, str, str, scoped_session]:
    '''
        The method sets up a flask app for launching hydrus.
        It sets up the environment for starting the server.

        :param adduser: expects a tuple (int,str) denoting user credentials
        :param api: string denoting the name of the api
        :param auth: boolean that determines if authenetication has to be used
        :param dburl: url to sqlite database
        :param hydradoc: click file object that points to the HYDRA doc
        :param port: integer that denotes the port to host the api
        :param serverurl: string to denote server url
        :return : (Flask app, Hydradoc, Severurl, api_name, session )
    '''
    DB_URL = dburl

    # Define the server URL, this is what will be displayed on the Doc
    HYDRUS_SERVER_URL = serverurl + ":" + str(port) + "/"

    # The name of the API or the EntryPoint, the api will be at
    # http://localhost/<API_NAME>
    API_NAME = api

    click.echo("Setting up the database")
    # Create a connection to the database you want to use
    engine = create_engine(DB_URL)

    click.echo("Creating models")
    # Add the required Models to the database
    Base.metadata.create_all(engine)
    '''
    Define the Hydra API Documentation
    NOTE: You can use your own API Documentation
    and create a HydraDoc object using doc_maker
    Or you may create your own HydraDoc Documentation using doc_writer [see
    hydrus/hydraspec/doc_writer_sample]
    '''
    click.echo("Creating the API Documentation")
    apidoc = doc_maker.create_doc(json.loads(hydradoc.read()),
                                  HYDRUS_SERVER_URL, API_NAME)

    # Start a session with the DB and create all classes needed by the
    # APIDoc
    session = scoped_session(sessionmaker(bind=engine))

    click.echo("Adding Classes and Properties")
    # Get all the classes from the doc
    # You can also pass dictionary defined in
    # hydrus/hydraspec/doc_writer_sample_output.py
    classes = doc_parse.get_classes(apidoc.generate())

    # Get all the properties from the classes
    properties = doc_parse.get_all_properties(classes)

    # Insert them into the database
    doc_parse.insert_classes(classes, session)
    doc_parse.insert_properties(properties, session)

    click.echo("Adding authorized users")
    add_user(id_=adduser[0], paraphrase=adduser[1], session=session)

    # Insert them into the database
    doc_parse.insert_classes(classes, session)
    doc_parse.insert_properties(properties, session)

    click.echo("Creating the application")
    # Create a Hydrus app with the API name you want, default will be
    # "api"
    app = app_factory(API_NAME)
    # Set the name of the API
    return (app, apidoc, HYDRUS_SERVER_URL, API_NAME, session)


def add_to_collection(object_: Dict[Any,Any], type_: str):
    """
       A function that adds the an object of a particular collection
       to the database.

       :param object_: a dictionary containing properties and type 
       :param type_: a string that denotes request type

    """
    click.echo(str(type(object_)) + " " + str(type(type_)))
    endpoint_ = checkEndpoint("PUT", type_)
    if endpoint_['method']:
        # If endpoint and PUT method is supported in the API
        if type_ in get_doc().collections:
            # If collection name in document's collections
            collection = get_doc().collections[type_]["collection"]

            # title of HydraClass object corresponding to collection
            obj_type = collection.class_.title

            if object_["@type"] == obj_type:
                # If the right Item type is being added to the
                # collection
                try:
                    # Insert object and return location in Header
                    object_id = crud.insert(
                        object_=object_, session=get_session())
                    response = "Object with ID %s successfully added" % (
                        object_id)
                    click.echo(response)
                    return True
                except Exception as e:
                    click.echo(str(e))
            else:
                click.echo("Data is invalid")
        elif type_ in get_doc().parsed_classes and\
                type_ + "Collection" not in get_doc().collections:
            # If type_ is in parsed_classes but is not a collection
            obj_type = getType(type_, "PUT")
            if object_["@type"] == obj_type:
                try:
                    object_id = crud.insert(
                        object_=object_, session=get_session())
                    response = "Object with ID %s successfully added" % (
                        object_id)
                    click.echo(response)
                    return True
                except Exception as e:
                    click.echo(str(e))
            else:
                click.echo("Data is invalid")
    return False
