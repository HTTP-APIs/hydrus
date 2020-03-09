"""Main route for the application"""

import logging
import sys
from os.path import dirname, abspath
# insert the ./app.py file path in the PYTHONPATH variable for imports to work
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from sqlalchemy import create_engine
from flask import request
from collections import defaultdict
from gevent.pywsgi import WSGIServer
from sqlalchemy.orm import sessionmaker

from hydrus.app_factory import app_factory
from hydrus.conf import (
    HYDRUS_SERVER_URL, API_NAME, DB_URL, APIDOC_OBJ, PORT, DEBUG)
from hydrus.data import doc_parse
from hydrus.data.db_models import Base, create_database_tables
from hydrus.data.exceptions import UserExists
from hydrus.data.user import add_user
from hydra_python_core import doc_maker
from hydrus.utils import (
    set_session, set_doc, set_hydrus_server_url,
    set_token, set_api_name, set_authentication)
from hydrus.socketio_factory import create_socket

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

# global dict to store mapping of each function to be run before
# specified route.
# stores in the form {'path1': {'method1': function_before_path1_for_method1}}
before_request_funcs = defaultdict(dict)


@app.before_request
def before_request_callback():
    path = request.path
    method = request.method
    global before_request_funcs
    func = before_request_funcs.get(path, {}).get(method, None)
    if func:
        func()


# decorator to define logic for custom before request methods
def custom_before_request(path, method):
    def wrapper(f):
        global before_request_funcs
        before_request_funcs[path][method] = f
        return f
    return wrapper


@custom_before_request('/api/MessageCollection', 'PUT')
def do_this_before_put_on_drone_collections():
    print("Do something before PUT request on MessageCollection")


@custom_before_request('/api/MessageCollection', 'GET')
def do_this_before_get_on_drone_collections():
    print("Do something before GET request on MessageCollection")


#
# Nested context managers
#
# Use authentication for all requests
# Set the API Documentation
# Set HYDRUS_SERVER_URL
# Set the Database session
with set_authentication(app, AUTH), set_token(app, TOKEN), \
     set_api_name(app, API_NAME), set_doc(app, apidoc), \
     set_hydrus_server_url(app, HYDRUS_SERVER_URL), set_session(app, session):
        if __name__ == "__main__":
            # this is run only if development server is run
            # Set the name of the API
            socketio.run(app=app, debug=True, port=PORT)
        else:
            # Start the Hydrus app
            http_server = WSGIServer(('', PORT), app)
            logger.info(f'Running server at port {PORT}')
            try:
                http_server.serve_forever()
            except KeyboardInterrupt:
                pass


