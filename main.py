"""Demo script for setting up Hydrus with any db and any API Doc."""

from hydrus.app import app_factory, set_session, set_doc, set_hydrus_server_url
from hydrus.data import doc_parse
from hydrus.hydraspec import doc_maker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hydrus.data.db_models import Base

import os
from hydrus.metadata.doc import doc     # Can be replaced by any API Documentation

# The database connection URL
# See http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html#sqlalchemy.create_engine for more info
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
DB_URL = 'sqlite:///{}'.format(db_path)

# Define the server URL, this is what will be displayed on the Doc
HYDRUS_SERVER_URL = "http://localhost:8080/"

# The port on which Hydrus should run
PORT = 8080

# The name of the API or the EntryPoint, the api will be at http://localhost/<API_NAME>
API_NAME = "serverapi"


if __name__ == "__main__":
    # Create a connection to the database you want to use
    engine = create_engine(DB_URL)

    # Add the required Models to the database
    Base.metadata.create_all(engine)

    # Define the Hydra API Documentation
    # NOTE: You can use your own API Documentation and create a HydraDoc object using doc_maker
    #       Or you may create your own HydraDoc Documentation using doc_writer [see hydrus/hydraspec/doc_writer_sample]
    apidoc = doc_maker.createDoc(doc, HYDRUS_SERVER_URL, API_NAME)

    # Start a session with the DB and create all classes needed by the APIDoc
    session = sessionmaker(bind=engine)()

    # Get all the classes from the doc
    classes = doc_parse.get_classes(apidoc.generate())     # You can also pass a dictionary as defined in hydrus/hydraspec/doc_writer_sample_output.py

    # Get all the properties from the classes
    properties = doc_parse.get_all_properties(classes)

    # Insert them into the database
    doc_parse.insert_classes(classes, session)
    doc_parse.insert_properties(properties, session)

    # Create a Hydrus app with the API name you want, default will be "api"
    app = app_factory(API_NAME)

    # Set the API Documentation
    with set_doc(app, apidoc):
        # Set HYDRUS_SERVER_URL
        with set_hydrus_server_url(app, HYDRUS_SERVER_URL):
            # Set the Database session
            with set_session(app, session):
                # Start the Hydrus app
                app.run(host='127.0.0.1', debug=True, port=8080)
