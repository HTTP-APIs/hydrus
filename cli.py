from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from hydrus.app import app_factory
from hydrus.utils import (set_session, set_doc, set_hydrus_server_url,
                            set_api_name, set_authentication)
from hydrus.data import doc_parse
from hydrus.hydraspec import doc_maker
from hydrus.data.db_models import Base
from hydrus.data.user import add_user
from gevent.wsgi import WSGIServer
import json
import click

@click.command()
@click.option("--adduser", "-u", default=tuple([1, "test"]),
                help="Adds a new user to the API.", nargs=2, type=(int, str))
@click.option("--api", "-a", default="serverapi",
                help="The API name.", type=str)
@click.option("--auth/--no-auth", default=True,
                help="Set authentication to True or False.")
@click.option("--hydradoc", "-d", default="doc.json",
                help="Location to HydraDocumentation (JSON) of server.",
                type=click.File('r'))
@click.option("--port", "-p", default=8080,
                help="The port the app is hosted at.", type=int)
@click.argument("serve", required=True)
def startserver(adduser, api, auth, hydradoc, port, serve):
    """Python Hydrus CLI"""
    # The database connection URL
    # See http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html#sqlalchemy.create_engine for more info
    # DB_URL = 'sqlite:///database.db'
    DB_URL = 'sqlite:///:memory:'

    # Define the server URL, this is what will be displayed on the Doc
    HYDRUS_SERVER_URL = "http://localhost:" + str(port) + "/"

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
    classes = doc_parse.get_classes(apidoc.generate())     # You can also pass dictionary defined in hydrus/hydraspec/doc_writer_sample_output.py

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
