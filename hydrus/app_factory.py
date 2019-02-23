from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from hydrus.resources import (Index, Vocab, Contexts, Entrypoint,
                              ItemCollection, Item, Items)


def app_factory(api_name: str = "api") -> Flask:
    """Create an app object."""

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key'
    CORS(app)
    app.url_map.strict_slashes = False
    api = Api(app)

    api.add_resource(Index, "/{}/".format(api_name), endpoint="api")
    api.add_resource(Vocab, "/{}/vocab".format(api_name), endpoint="vocab")
    api.add_resource(
        Contexts,
        "/{}/contexts/<string:category>.jsonld".format(api_name),
        endpoint="contexts")
    api.add_resource(
        Entrypoint,
        "/{}/contexts/EntryPoint.jsonld".format(api_name),
        endpoint="main_entrypoint")
    api.add_resource(
        ItemCollection,
        "/{}/<string:path>".format(api_name),
        endpoint="item_collection")
    api.add_resource(
        Item,
        "/{}/<string:path>/<uuid:id_>".format(api_name),
        endpoint="item")
    api.add_resource(
        Items,
        "/{}/<string:path>/add/<int_list>".format(api_name),
        "/{}/<string:path>/add".format(api_name),
        "/{}/<string:path>/delete/<int_list>".format(api_name))

    return app
