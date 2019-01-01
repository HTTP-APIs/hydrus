import json
from typing import Tuple
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from hydrus.app import app_factory
from hydrus.utils import (set_session, set_doc, set_hydrus_server_url,
                          set_token, set_api_name, set_authentication)
from hydrus.data import doc_parse
from hydrus.data.exceptions import UserExists
from hydrus.hydraspec import doc_maker
from hydrus.data.db_models import Base
from hydrus.data.user import add_user
from gevent.pywsgi import WSGIServer
from hydrus.parser.openapi_parser import parse
# from hydrus.examples.drones.doc import doc
from importlib.machinery import SourceFileLoader


doc = SourceFileLoader("doc", "./examples/drones/doc.py").load_module().doc

HYDRUS_SERVER_URL = "http://localhost:8080/"
API_NAME = "serverapi"
PORT = 8080

engine = create_engine('sqlite:///database.db')

Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

apidoc = doc_maker.create_doc(doc, HYDRUS_SERVER_URL, API_NAME)

classes = doc_parse.get_classes(apidoc.generate())

# Get all the properties from the classes
properties = doc_parse.get_all_properties(classes)

# Insert them into the database
doc_parse.insert_classes(classes, session)
doc_parse.insert_properties(properties, session)

AUTH = True
TOKEN = True

if AUTH:
    try:
        add_user(id_=1, paraphrase="test", session=session)
    except UserExists:
        pass
# Insert them into the database
doc_parse.insert_classes(classes, session)
doc_parse.insert_properties(properties, session)

# Create a Hydrus app with the API name you want, default will be "api"
app = app_factory(API_NAME)
# Set the name of the API
with set_authentication(app, AUTH):
    # Use authentication for all requests
    with set_token(app, TOKEN):
        with set_api_name(app, API_NAME):
            # Set the API Documentation
            with set_doc(app, apidoc):
                # Set HYDRUS_SERVER_URL
                with set_hydrus_server_url(app, HYDRUS_SERVER_URL):
                    # Set the Database session
                    with set_session(app, session):
                        # Start the Hydrus app
                        http_server = WSGIServer(('', PORT), app)
                        print("running server at port", PORT)
                        try:
                            http_server.serve_forever()
                        except KeyboardInterrupt:
                            pass
