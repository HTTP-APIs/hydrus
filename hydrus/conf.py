"""
Global variables are loaded or set here:
    DEBUG
    PORT
    API_NAME
    DB_URL
    APIDOC_OBJ
    HYDRUS_SERVER_URL
    FOUND_DOC
"""
import os
import json
import yaml
import logging
from os.path import abspath, dirname
from pathlib import Path
from importlib.machinery import SourceFileLoader
from hydra_openapi_parser.openapi_parser import parse

logger = logging.getLogger(__file__)

try:
    DEBUG = bool(os.environ["DEBUG"])
except KeyError:
    DEBUG = False

# load form environment (as many globals as possible shall be in
# environment configuration)

PORT = int(os.environ["PORT"]) if "PORT" in dict(os.environ).keys() else 8080
API_NAME = os.environ["API_NAME"] if "API_NAME" in dict(os.environ).keys() else "api"
DB_URL = (
    os.environ["DB_URL"]
    if "DB_URL" in dict(os.environ).keys()
    else "sqlite:///database.db"
)


def get_apidoc_path():
    """
    Get the path of the apidoc.

    :return - Tuple (path, boolean). path denotes path of the apidoc.
    If apidoc is not present at specified path then it falls back at sample apidoc.
    boolean is true if the apidoc is present at the specified path.
    boolean is false if sample apidoc is being used.
    """
    cwd_path = Path(dirname(dirname(abspath(__file__))))
    try:
        apidoc_env = os.environ["APIDOC_REL_PATH"]
        apidoc_path = cwd_path / Path(apidoc_env)
        found_doc = True
    except KeyError:
        found_doc = False
        apidoc_path = cwd_path / "hydrus" / "samples" / "hydra_doc_sample.py"
    return (apidoc_path, found_doc)


def load_apidoc(path):
    """
    Parses docs of .jsonld, .py, .yaml format and loads apidoc from the given path.

    :param path - Path for the apidoc to be loaded
    :return - apidoc
    :Raises:
        FileNotFoundError: If the wrong path of hydradoc is specified.
        BaseException: If hydradoc is specified in wrong format.
    """
    path = str(path)
    try:
        apidoc_format = path.split(".")[-1]
        if apidoc_format == "jsonld":
            with open(path, "r") as f:
                api_doc = json.load(f)
        elif apidoc_format == "py":
            api_doc = SourceFileLoader("doc", path).load_module().doc
        elif apidoc_format == "yaml":
            with open(path, "r") as stream:
                api_doc = parse(yaml.load(stream))
        else:
            raise (
                "Error - hydradoc format not supported."
                "The supported formats are .py, .jsonld and .yaml"
            )

        logger.info(f"APIDOC path loaded from: {path}")
        return api_doc
    except FileNotFoundError:
        logger.critical(
            f"No Hydra ApiDoc file to load has been found"
            f" at {path}. Cannot set APIDOC_OBJ"
        )
        raise
    except BaseException:
        logger.critical("Problem parsing specified hydradoc file")
        raise


def get_host_domain():
    """
    Returns host domain.
    """
    HOST_DOMAIN = f"http://localhost:{PORT}"
    return HOST_DOMAIN


(path, FOUND_DOC) = get_apidoc_path()
APIDOC_OBJ = load_apidoc(path)
HYDRUS_SERVER_URL = f"http://localhost:{PORT}/"
