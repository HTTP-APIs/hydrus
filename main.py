"""Demo script for setting up Hydrus with any db and any API Doc."""

from hydrus.app import app, set_session, set_doc, set_hydrus_server_url
from hydrus.data import doc_parse
from hydrus.hydraspec import doc_maker
from hydrus.settings import HYDRUS_SERVER_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hydrus.data.db_models import Base

from hydrus.metadata.doc import doc     # Can be replaced by any API Documentation

# Create a connection to the database you want to use
engine = create_engine('sqlite:///sqlalchemy_example.db')

# Add the required Models to the database
Base.metadata.create_all(engine)

# Define the Hydra API Documentation
# NOTE: You can use your own API Documentation and create a HydraDoc object using doc_maker
#       Or you may create your own HydraDoc Documentation using doc_writer [see hydrus/hydraspec/doc_writer_sample]
apidoc = doc_maker.createDoc(doc)

# Start a session with the DB and create all classes needed by the APIDoc
session = sessionmaker(bind=engine)()

# Get all the classes from the doc
classes = doc_parse.get_classes(apidoc.generate())     # You can also pass a dictionary as defined in hydrus/hydraspec/doc_writer_sample_output.py

# Get all the properties from the classes
properties = doc_parse.get_all_properties(classes)

# Insert them into the database
doc_parse.insert_classes(classes, session)
doc_parse.insert_properties(properties, session)

# Set the API Documentation
with set_doc(app, apidoc):
    # Set HYDRUS_SERVER_URL
    with set_hydrus_server_url(app, HYDRUS_SERVER_URL):

        # Set the DB session
        with set_session(app, session):
        # Start Hydrus
            app.run(host='127.0.0.1', debug=True, port=8080)
