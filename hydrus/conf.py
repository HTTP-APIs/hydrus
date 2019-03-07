"""
Global variables are loaded or set here:
    DEBUG
    PORT
    API_NAME
    DB_URL
    APIDOC_OBJ
    HYDRUS_SERVER_URL
"""
import os
import logging

from os.path import abspath, dirname
from pathlib import Path

from importlib.machinery import SourceFileLoader

logger = logging.getLogger(__file__)

try:
    DEBUG = bool(os.environ['DEBUG'])
except KeyError:
    DEBUG = False

# load form environment (as many globals as possible shall be in
# environment configuration)
PORT = int(os.environ['PORT']) if 'PORT' in dict(os.environ).keys() else 8080
API_NAME = os.environ['API_NAME'] if 'API_NAME' in dict(os.environ).keys() else 'api'
DB_URL = os.environ['DB_URL'] if 'DB_URL' in dict(os.environ).keys() else 'sqlite:///database.db'


# source for the Hydra documentation file can be defined as
# as environment variable, otherwise it falls back to the example
# TODO: why is this a Python module instead of being a JSON-LD file?
cwd_path = Path(dirname(dirname(abspath(__file__))))
try:
    # try to load the path specified in environment variable
    apidoc_env = os.environ['APIDOC_REL_PATH']
    apidoc_path = cwd_path / Path(apidoc_env)
except KeyError:
    # if it is not set, use the example doc
    apidoc_path = cwd_path / 'examples' / 'drones' / 'doc.py'

try:
    APIDOC_OBJ = SourceFileLoader(
        'doc',
        str(apidoc_path)).load_module().doc
    logger.info('APIDOC path loaded from: {}'.format(apidoc_path))
except FileNotFoundError:
    logger.critical('No Hydra ApiDoc file to load has been found at {}. '
                    'Cannot set APIDOC_OBJ'.format(apidoc_path))
    raise

HYDRUS_SERVER_URL = 'http://localhost:{}/'.format(PORT)
