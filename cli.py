from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from hydrus.app_factory import app_factory
from hydrus.utils import (set_session, set_doc, set_hydrus_server_url,
                          set_token, set_api_name, set_authentication,
                          set_page_size, set_pagination)
from hydrus.data import doc_parse
from hydra_python_core import doc_maker
from hydrus.data.db_models import Base
from hydrus.data.user import add_user
from hydrus.data.exceptions import UserExists
from gevent.pywsgi import WSGIServer
from hydra_openapi_parser.openapi_parser import parse
from hydrus.samples.hydra_doc_sample import doc as api_document
from importlib.machinery import SourceFileLoader
from typing import Tuple
import json
import click
import yaml


@click.command()
@click.option("--adduser", "-u", default=tuple([1, "test"]),
              help="Adds a new user to the API.", nargs=2, type=(int, str))
@click.option("--api", "-a", default="serverapi",
              help="The API name.", type=str)
@click.option("--auth/--no-auth", default=True,
              help="Set authentication to True or False.")
@click.option("--dburl", default="sqlite:///:memory:",
              help="Set database url", type=str)
@click.option("--hydradoc", "-d", default=None,
              help="Location to HydraDocumentation (JSON-LD) of server.",
              type=str)
@click.option("--port", "-p", default=8080,
              help="The port the app is hosted at.", type=int)
@click.option("--pagesize", "-ps", default=10,
              help="Maximum size of a page(view)", type=int)
@click.option("--pagination/--no-pagination", default=True,
              help="Enable or disable pagination.")
@click.option("--token/--no-token", default=True,
              help="Toggle token based user authentication.")
@click.option("--serverurl", default="http://localhost",
              help="Set server url", type=str)
@click.argument("serve", required=True)
def startserver(adduser: Tuple, api: str, auth: bool, dburl: str, pagination: bool,
                hydradoc: str, port: int, pagesize: int, serverurl: str, token: bool,
                serve: None) -> None:
    """
    Python Hydrus CLI

    :param openapi:         : Sets the link to the Open Api Doc file.
    :param adduser <tuple>  : Contains the user credentials.
    :param api <str>        : Sets the API name for the server.
    :param auth <bool>      : Toggles the authentication.
    :param dburl <str>      : Sets the database URL.
    :param hydradoc <str>   : Sets the link to the HydraDoc file
                            (Supported formats - [.py, .jsonld, .yaml])
    :param port <int>       : Sets the API server port.
    :param serverurl <str>  : Sets the API server url.
    :param token <bool>     : Toggle token based user auth.
    :param serve            : Starts up the server.

    :return                 : None.


    Raises:
        Error: If `hydradoc` is not of a supported format[.py, .jsonld, .yaml].

    """
    # The database connection URL
    # See http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html for more info
    # DB_URL = 'sqlite:///database.db'
    DB_URL = dburl

    # Define the server URL, this is what will be displayed on the Doc
    HYDRUS_SERVER_URL = "{}:{}/".format(serverurl, str(port))

    # The name of the API or the EntryPoint, the api will be at
    # http://localhost/<API_NAME>
    API_NAME = api

    click.echo("Setting up the database")
    # Create a connection to the database you want to use
    engine = create_engine(DB_URL)

    click.echo("Creating models")
    # Add the required Models to the database
    Base.metadata.create_all(engine)

    # Define the Hydra API Documentation
    # NOTE: You can use your own API Documentation and create a HydraDoc object
    # using doc_maker or you may create your own HydraDoc Documentation using
    # doc_writer [see hydra_python_core/doc_writer_sample]
    click.echo("Creating the API Documentation")

    if hydradoc:
        # Getting hydradoc format
        # Currently supported formats [.jsonld, .py, .yaml]
        try:
            hydradoc_format = hydradoc.split(".")[-1]
            if hydradoc_format == 'jsonld':
                with open(hydradoc, 'r') as f:
                    doc = json.load(f)
            elif hydradoc_format == 'py':
                doc = SourceFileLoader(
                    "doc", hydradoc).load_module().doc
            elif hydradoc_format == 'yaml':
                with open(hydradoc, 'r') as stream:
                    doc = parse(yaml.load(stream))
            else:
                raise("Error - hydradoc format not supported.")

            click.echo("Using %s as hydradoc" % hydradoc)
            apidoc = doc_maker.create_doc(doc,
                                          HYDRUS_SERVER_URL, API_NAME)

        except BaseException:
            click.echo("Problem parsing specified hydradoc file, "
                       "using sample hydradoc as default.")
            apidoc = doc_maker.create_doc(api_document,
                                          HYDRUS_SERVER_URL, API_NAME)
    else:
        click.echo("No hydradoc specified, using sample hydradoc as default.\n"
                   "For creating api documentation see this "
                   "https://www.hydraecosystem.org/01-Usage.html#newdoc\n"
                   "You can find the example used in hydrus/samples/hydra_doc_sample.py")
        apidoc = doc_maker.create_doc(
            api_document, HYDRUS_SERVER_URL, API_NAME)

    # Start a session with the DB and create all classes needed by the APIDoc
    session = scoped_session(sessionmaker(bind=engine))

    click.echo("Adding Classes and Properties")
    # Get all the classes from the doc
    # You can also pass dictionary defined in
    # hydra_python_core/doc_writer_sample_output.py
    classes = doc_parse.get_classes(apidoc.generate())

    # Get all the properties from the classes
    properties = doc_parse.get_all_properties(classes)

    # Insert them into the database
    doc_parse.insert_classes(classes, session)
    doc_parse.insert_properties(properties, session)

    # Add authorized users and pass if they already exist
    click.echo("Adding authorized users")
    try:
        add_user(id_=adduser[0], paraphrase=adduser[1], session=session)
    except UserExists:
        pass

    # Insert them into the database
    doc_parse.insert_classes(classes, session)
    doc_parse.insert_properties(properties, session)

    click.echo("Creating the application")
    # Create a Hydrus app with the API name you want, default will be "api"
    app = app_factory(API_NAME)
    # Set the name of the API
    click.echo("Starting the application")
    with set_authentication(app, auth):
        # Use authentication for all requests
        with set_token(app, token):
            with set_api_name(app, api):
                # Set the API Documentation
                with set_doc(app, apidoc):
                    # Set HYDRUS_SERVER_URL
                    with set_hydrus_server_url(app, HYDRUS_SERVER_URL):
                        # Set the Database session
                        with set_session(app, session):
                            # Enable/disable pagination
                            with set_pagination(app, pagination):
                                # Set page size of a collection view
                                with set_page_size(app, pagesize):
                                    # Start the hydrus app
                                    http_server = WSGIServer(('', port), app)
                                    click.echo("Server running at:")
                                    click.echo(
                                        "{}{}".format(
                                            HYDRUS_SERVER_URL,
                                            API_NAME))
                                    try:
                                        http_server.serve_forever()
                                    except KeyboardInterrupt:
                                        pass


if __name__ == "__main__":
    startserver()
