from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from hydrus.app import app_factory
from hydrus.utils import (set_session, set_doc, set_hydrus_server_url,
                          set_token, set_api_name, set_authentication)
from hydrus.data import doc_parse
from hydrus.hydraspec import doc_maker
from hydrus.data.db_models import Base
from hydrus.data.user import add_user
from gevent.wsgi import WSGIServer
from typing import Tuple
import json
import click


@click.command()
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
              help="The port the app is hosted at.", type=int)
@click.option("--token/--no-token", default=True,
              help="Toggle token based user authentication.")
@click.option("--serverurl", default="http://localhost",
              help="Set server url", type=str)
@click.argument("serve", required=True)
def startserver(adduser: Tuple, api: str, auth: bool, dburl: str,
                hydradoc: str, port: int, serverurl: str, token: bool,
                serve: None) -> None:
    """
    Python Hydrus CLI

    :param adduser <tuple>  : Contains the user credentials.
    :param api <str>                    : Sets the API name for the server.
    :param auth <bool>                  : Toggles the authentication.
    :param dburl <str>                  : Sets the database URL.
    :param hydradoc <str>               : Sets the link to the HydraDoc file.
    :param port <int>                   : Sets the API server port.
    :param serverurl <str>              : Sets the API server url.
    :param token <bool>                 : Toggle token based user auth.
    :param serve                        : Starts up the server.

    :return                             : None.
    """
    # The database connection URL
    # See http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html#sqlalchemy.create_engine for more info
    # DB_URL = 'sqlite:///database.db'
    DB_URL = dburl

    # Define the server URL, this is what will be displayed on the Doc
    HYDRUS_SERVER_URL = "{}:{}/".format(serverurl, str(port))

    # The name of the API or the EntryPoint, the api will be at http://localhost/<API_NAME>
    API_NAME = api

    click.echo("Setting up the database")
    # Create a connection to the database you want to use
    engine = create_engine(DB_URL)

    click.echo("Creating models")
    # Add the required Models to the database
    Base.metadata.create_all(engine)

    # Define the Hydra API Documentation
    # NOTE: You can use your own API Documentation and create a HydraDoc object using doc_maker
    #       Or you may create your own HydraDoc Documentation using doc_writer [see hydrus/hydraspec/doc_writer_sample]
    click.echo("Creating the API Documentation")
    apidoc = doc_maker.create_doc(json.loads(hydradoc.read()),
                                  HYDRUS_SERVER_URL, API_NAME)

    # Start a session with the DB and create all classes needed by the APIDoc
    session = scoped_session(sessionmaker(bind=engine))

    click.echo("Adding Classes and Properties")
    # Get all the classes from the doc
    # You can also pass dictionary defined in hydrus/hydraspec/doc_writer_sample_output.py
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
                            # Start the Hydrus app
                            http_server = WSGIServer(('', port), app)
                            click.echo("Server running at:")
                            click.echo(HYDRUS_SERVER_URL + API_NAME)
                            try:
                                http_server.serve_forever()
                            except KeyboardInterrupt:
                                pass


if __name__ == "__main__":
    startserver()
