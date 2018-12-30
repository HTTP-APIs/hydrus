from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from hydrus.resources import Index, Vocab, Contexts, Entrypoint, ItemCollection, Item, Items


def app_factory(API_NAME: str = "api") -> Flask:
    """Create an app object."""

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key'
    CORS(app)
    app.url_map.strict_slashes = False
    api = Api(app)

    api.add_resource(Index, f"/{API_NAME}/", endpoint="api")
    api.add_resource(Vocab, f"/{API_NAME}/vocab", endpoint="vocab")
    api.add_resource(Contexts,
                     f"/{API_NAME}/contexts/<string:category>.jsonld", endpoint="contexts")
    api.add_resource(Entrypoint,
                     f"/{API_NAME}/contexts/EntryPoint.jsonld", endpoint="main_entrypoint")
    api.add_resource(ItemCollection,
                     f"/{API_NAME}/<string:path>", endpoint="item_collection")
    api.add_resource(Item,
                     f"/{API_NAME}/<string:path>/<uuid:id_>", endpoint="item")
    api.add_resource(Items, f"/{API_NAME}/<string:path>/add/<int_list>",
                     f"/{API_NAME}/<string:path>/add",
                     f"/{API_NAME}/<string:path>/delete/<int_list>")

    return app
