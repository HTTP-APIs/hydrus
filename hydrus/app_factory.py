from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from hydrus.resources import (Index, Vocab, Contexts, Entrypoint,
                              ItemCollection, Item, Items)


def app_factory(API_NAME: str = "api") -> Flask:
    """Create an app object."""

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key'
    CORS(app)
    app.url_map.strict_slashes = False
    api = Api(app)

    api.add_resource(Index, "/" + API_NAME + "/", endpoint="api")
    api.add_resource(Vocab, "/" + API_NAME + "/vocab", endpoint="vocab")
    api.add_resource(Contexts, "/" + API_NAME +
                     "/contexts/<string:category>.jsonld", endpoint="contexts")
    api.add_resource(Entrypoint, "/" + API_NAME +
                     "/contexts/EntryPoint.jsonld", endpoint="main_entrypoint")
    api.add_resource(ItemCollection, "/" + API_NAME +
                     "/<string:path>", endpoint="item_collection")
    api.add_resource(Item, "/" + API_NAME +
                     "/<string:path>/<uuid:id_>", endpoint="item")
    api.add_resource(Items, "/" + API_NAME +
                     "/<string:path>/add/<int_list>", "/" + API_NAME +
                     "/<string:path>/add", "/" + API_NAME +
                     "/<string:path>/delete/<int_list>")

    return app
