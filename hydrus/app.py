"""Main route for the application"""

import logging

from sqlalchemy import create_engine

from gevent.pywsgi import WSGIServer
from sqlalchemy.orm import sessionmaker

from hydrus.app_factory import app_factory
from hydrus.conf import HYDRUS_SERVER_URL, API_NAME, DB_URL, APIDOC_OBJ, PORT, DEBUG
from hydrus.data import doc_parse
from hydrus.data.db_models import Base, create_database_tables
from hydrus.data.exceptions import UserExists
from hydrus.data.user import add_user
from hydra_python_core import doc_maker
from hydrus.utils import (
    set_session,
    set_doc,
    set_hydrus_server_url,
    set_token,
    set_api_name,
    set_authentication,
)
from hydrus.extensions.socketio_factory import create_socket

logger = logging.getLogger(__file__)

# TODO: loading the engine and creating the tables should be handled better
engine = create_engine(DB_URL)
session = sessionmaker(bind=engine)()

#
# Load ApiDoc with doc_maker
#
apidoc = doc_maker.create_doc(APIDOC_OBJ, HYDRUS_SERVER_URL, API_NAME)
classes = doc_parse.get_classes(apidoc)
try:
    Base.metadata.drop_all(engine)
    create_database_tables(classes)
    Base.metadata.create_all(engine)
except Exception:
    pass

AUTH = True
TOKEN = True

if AUTH:
    try:
        add_user(id_=1, paraphrase="test", session=session)
    except UserExists:
        pass

# Create a Hydrus app
app = app_factory(API_NAME)
socketio = create_socket(app, session)
#
# Nested context managers
#
# Use authentication for all requests
# Set the API Documentation
# Set HYDRUS_SERVER_URL
# Set the Database session
with set_authentication(app, AUTH), set_token(app, TOKEN), set_api_name(
    app, API_NAME
), set_doc(app, apidoc), set_hydrus_server_url(app, HYDRUS_SERVER_URL), set_session(
    app, session
):
    if __name__ == "__main__":
        # this is run only if development server is run
        # Set the name of the API
        socketio.run(app=app, debug=True, port=PORT)
    else:
        # Start the Hydrus app
        http_server = WSGIServer(("", PORT), app)
        logger.info(f"Running server at port {PORT}")
        try:
            http_server.serve_forever()
        except KeyboardInterrupt:
            pass
