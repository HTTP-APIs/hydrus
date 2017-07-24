"""Demo script for setting up Hydrus with any db and any API Doc."""

from hydrus.app import app, set_session, set_doc
from hydrus.data import doc_parse
from hydrus.metadata.doc_gen import doc_gen
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hydrus.data.db_models import Base

# Create a connection to the database you want to use
engine = create_engine('sqlite:///sqlalchemy_example.db')

# Add the required Models to the database
Base.metadata.create_all(engine)

# Define the Hydra API Documentation [see hydrus/hydraspec/doc_writer_sample for more info]
doc = doc_gen("api", "http://localhost:8080/")

# Start a session with the DB and create all classes needed by the APIDoc
session = sessionmaker(bind=engine)()

# Get all the classes from the doc
classes = doc_parse.get_classes(doc.generate())     # You can also pass a dictionary as defined in hydrus/hydraspec/doc_writer_sample_output.py

# Get all the properties from the classes
properties = doc_parse.get_all_properties(classes)

# Insert them into the database
doc_parse.insert_classes(classes, session)
doc_parse.insert_properties(properties, session)

# Set the API Documentation
with set_doc(app, doc):
    # Set the DB session
    with set_session(app, session):
        # Start Hydrus
        app.run(host='127.0.0.1', debug=True, port=8080)
