"""Demo script for setting up Hydrus with any db and any API Doc."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from hydrus.app import app_factory
from hydrus.utils import set_session, set_doc, set_hydrus_server_url, set_api_name, set_authentication, set_token
from hydrus.data import doc_parse
from hydrus.hydraspec import doc_maker
from hydrus.data.db_models import Base
from hydrus.data.user import add_user
from doc import doc
from gevent.wsgi import WSGIServer


if __name__ == "__main__":
    # The database connection URL
    # See http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html#sqlalchemy.create_engine for more info
    # DB_URL = 'sqlite:///database.db'
    DB_URL = 'sqlite:///:memory:'

    # Define the server URL, this is what will be displayed on the Doc
    HYDRUS_SERVER_URL = "http://localhost:8080/"

    # The name of the API or the EntryPoint, the api will be at
    # http://localhost/<API_NAME>
    API_NAME = "serverapi"

    print("Setting up the database")
    # Create a connection to the database you want to use
    engine = create_engine(DB_URL)

    print("Creating models")
    # Add the required Models to the database
    Base.metadata.create_all(engine)

    # Define the Hydra API Documentation
    # NOTE: You can use your own API Documentation and create a HydraDoc object using doc_maker
    # Or you may create your own HydraDoc Documentation using doc_writer [see
    # hydrus/hydraspec/doc_writer_sample]
    print("Creating the API Documentation")
    apidoc = doc_maker.create_doc(doc, HYDRUS_SERVER_URL, API_NAME)

    # Start a session with the DB and create all classes needed by the APIDoc
    session = scoped_session(sessionmaker(bind=engine))

    print("Adding Classes and Properties")
    # Get all the classes from the doc
    # You can also pass dictionary defined in
    # hydrus/hydraspec/doc_writer_sample_output.py
    classes = doc_parse.get_classes(apidoc.generate())

    # Get all the properties from the classes
    properties = doc_parse.get_all_properties(classes)

    print("Adding authorized users")
    add_user(id_=1, paraphrase="test", session=session)

    # Insert them into the database
    doc_parse.insert_classes(classes, session)
    doc_parse.insert_properties(properties, session)

    print("Creating the application")
    # Create a Hydrus app with the API name you want, default will be "api"
    app = app_factory(API_NAME)
    # Set the name of the API
    print("Starting the application")
    with set_authentication(app, True):
        # Use authentication for all requests
        with set_token(app, True):
            with set_api_name(app, "serverapi"):
                # Set the API Documentation
                with set_doc(app, apidoc):
                    # Set HYDRUS_SERVER_URL
                    with set_hydrus_server_url(app, HYDRUS_SERVER_URL):
                        # Set the Database session
                        with set_session(app, session):
                            # Start the Hydrus app
                            http_server = WSGIServer(('', 8080), app)
                            print("Server running at:")
                            print("{}{}".format(HYDRUS_SERVER_URL, API_NAME))
                            try:
                                http_server.serve_forever()
                            except KeyboardInterrupt:
                                pass
