from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from hydrus.app_factory import app_factory
from hydrus.extensions.socketio_factory import create_socket
from hydrus.utils import (
    set_session,
    set_doc,
    set_hydrus_server_url,
    set_token,
    set_api_name,
    set_authentication,
    set_page_size,
    set_pagination,
)
from hydrus.data import doc_parse
from hydra_python_core import doc_maker
from hydrus.data.db_models import Base, create_database_tables
from hydrus.data.user import add_user
from hydrus.data.exceptions import UserExists
from hydrus.extensions.stale_records_cleanup import remove_stale_modification_records
from hydra_openapi_parser.openapi_parser import parse
from importlib.machinery import SourceFileLoader
import json
import click
import yaml
from hydrus.conf import APIDOC_OBJ, FOUND_DOC


@click.group()
def startserver():
    """
    Python Hydrus CLI.
    """
    pass


@startserver.command()
@click.option(
    "--adduser",
    "-u",
    default=tuple([1, "test"]),
    help="Adds a new user to the API.",
    nargs=2,
    type=(int, str),
)
@click.option("--api", "-a", default="serverapi", help="The API name.", type=str)
@click.option(
    "--auth/--no-auth", default=True, help="Set authentication to True or False."
)
@click.option(
    "--dburl", default="sqlite:///database.db", help="Set database url.", type=str
)
@click.option(
    "--hydradoc",
    "-d",
    default=None,
    help="Location to HydraDocumentation (JSON-LD) of server.",
    type=str,
)
@click.option(
    "--port", "-p", default=8080, help="The port the app is hosted at.", type=int
)
@click.option(
    "--pagesize", "-ps", default=10, help="Maximum size of a page(view)", type=int
)
@click.option(
    "--pagination/--no-pagination", default=True, help="Enable or disable pagination."
)
@click.option(
    "--token/--no-token", default=True, help="Toggle token based user authentication."
)
@click.option(
    "--serverurl", default="http://localhost", help="Set server url", type=str
)
@click.option(
    "--use-db/--no-use-db", default=False, help="Use previously existing database"
)
@click.option(
    "--stale_records_removal_interval",
    default=900,
    help="Interval period between removal of stale modification records.",
    type=int,
)
def serve(
    adduser: tuple,
    api: str,
    auth: bool,
    dburl: str,
    pagination: bool,
    hydradoc: str,
    port: int,
    pagesize: int,
    serverurl: str,
    token: bool,
    use_db: bool,
    stale_records_removal_interval: int,
) -> None:
    """
    Starts up the server.
    \f

    :param adduser <tuple>  : Contains the user credentials.
    :param api <str>        : Sets the API name for the server.
    :param auth <bool>      : Toggles the authentication.
    :param dburl <str>      : Sets the database URL.
    :param pagination <bool>: Toggles the pagination.
    :param hydradoc <str>   : Sets the link to the HydraDoc file
                              (Supported formats - [.py, .jsonld, .yaml])
    :param port <int>       : Sets the API server port.
    :param pagesize <int>   : Sets maximum size of page(view).
    :param serverurl <str>  : Sets the API server url.
    :param token <bool>     : Toggle token based user auth.
    :stable_records_removal_interval <int> : Interval period between removal
                                             of stale modification records.

    :return                 : None

    Raises:
        Error: If `hydradoc` is not of a supported format[.py, .jsonld, .yaml].

    """
    # The database connection URL
    # See http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html for more info
    # DB_URL = 'sqlite:///database.db'
    DB_URL = dburl
    # Define the server URL, this is what will be displayed on the Doc
    HYDRUS_SERVER_URL = f"{serverurl}:{str(port)}/"

    # The name of the API or the EntryPoint, the api will be at
    # http://localhost/<API_NAME>
    API_NAME = api
    click.echo("Setting up the database")
    # Create a connection to the database you want to use
    engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
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
            if hydradoc_format == "jsonld":
                with open(hydradoc, "r") as f:
                    doc = json.load(f)
            elif hydradoc_format == "py":
                doc = SourceFileLoader("doc", hydradoc).load_module().doc
            elif hydradoc_format == "yaml":
                with open(hydradoc, "r") as stream:
                    doc = parse(yaml.load(stream))
            else:
                raise ("Error - hydradoc format not supported.")

            click.echo(f"Using {hydradoc} as hydradoc")
            apidoc = doc_maker.create_doc(doc, HYDRUS_SERVER_URL, API_NAME)

        except BaseException:
            if FOUND_DOC:
                click.echo(
                    "Problem parsing specified hydradoc file"
                    "Using hydradoc from environment variable"
                )
            else:
                click.echo(
                    "Problem parsing specified hydradoc file, "
                    "using sample hydradoc as default."
                )

            apidoc = doc_maker.create_doc(APIDOC_OBJ, HYDRUS_SERVER_URL, API_NAME)
    else:
        if FOUND_DOC:
            click.echo(
                "No hydradoc specified, using hydradoc from environment variable."
            )
        else:
            click.echo(
                "No hydradoc specified, using sample hydradoc as default.\n"
                "For creating api documentation see this "
                "https://www.hydraecosystem.org/01-Usage.html#newdoc\n"
                "You can find the example used in hydrus/samples/hydra_doc_sample.py"
            )

        apidoc = doc_maker.create_doc(APIDOC_OBJ, HYDRUS_SERVER_URL, API_NAME)

    # Start a session with the DB and create all classes needed by the APIDoc
    session = scoped_session(sessionmaker(bind=engine))

    # Get all the classes from the doc
    # You can also pass dictionary defined in
    # hydra_python_core/doc_writer_sample_output.py
    classes = doc_parse.get_classes(apidoc)
    # Insert them into the database
    if use_db is False:
        Base.metadata.drop_all(engine)
        click.echo("Adding Classes and Properties")
        create_database_tables(classes)
        click.echo("Creating models")
        Base.metadata.create_all(engine)

    # Add authorized users and pass if they already exist
    click.echo("Adding authorized users")
    try:
        add_user(id_=adduser[0], paraphrase=adduser[1], session=session)
    except UserExists:
        pass

    # Insert them into the database

    click.echo("Creating the application")
    # Create a Hydrus app with the API name you want, default will be "api"
    app = app_factory(API_NAME, apidoc.doc_name)
    # Set the name of the API
    # Create a socket for the app
    socketio = create_socket(app, session)
    click.echo("Starting the application")

    #
    # Nested context managers
    #
    # Use authentication for all requests
    # Set the API Documentation
    # Set HYDRUS_SERVER_URL
    # Set the Database session
    # Enable/disable pagination
    # Set page size of a collection view
    with set_authentication(app, auth) as _, set_token(app, token) as _, set_api_name(
        app, api
    ) as _, set_doc(app, apidoc) as _, set_hydrus_server_url(
        app, HYDRUS_SERVER_URL
    ) as _, set_session(
        app, session
    ) as _, set_pagination(
        app, pagination
    ) as _, set_page_size(
        app, pagesize
    ) as _:
        # Run a thread to remove stale modification records at some
        # interval of time.
        remove_stale_modification_records(session, stale_records_removal_interval)
        # Start the hydrus app
        socketio.run(app, port=port)
        click.echo("Server running at:")
        click.echo(f"{HYDRUS_SERVER_URL}{API_NAME}")


if __name__ == "__main__":
    startserver()
