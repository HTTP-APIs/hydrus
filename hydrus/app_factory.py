from flask import Flask

import yaml
from os.path import dirname
from pathlib import Path


def app_factory(api_name: str = "api", vocab_route: str = "vocab") -> Flask:
    """
    Create an app object
    :param api_name : Name of the api
    :param vocab_route : The route at which the vocab of the apidoc is present
    :return : API with all routes directed at /[api_name].
    """
    from flask import redirect
    from flask_cors import CORS
    from flask_restful import Api
    from hydrus.resources import (
        Index,
        Vocab,
        Contexts,
        Entrypoint,
        ItemCollection,
        Item,
    )

    app = Flask(__name__)

    config_dct = None
    with open(Path(dirname(dirname(__file__))) / Path("config.yml"), "r") as stream:
        config_dct = yaml.safe_load(stream)
    app.config["SECRET_KEY"] = config_dct["security"]["secret"]

    CORS(app)
    app.url_map.strict_slashes = False
    api = Api(app)

    # Redirecting root_path to root_path/api_name
    if api_name:

        @app.route("/")
        def root_url():
            return redirect(f"/{api_name}/")

    api.add_resource(Index, f"/{api_name}/", endpoint="api")
    api.add_resource(Vocab, f"/{api_name}/{vocab_route}", endpoint="vocab")
    api.add_resource(
        Contexts, f"/{api_name}/contexts/<string:category>.jsonld", endpoint="contexts"
    )
    api.add_resource(
        Entrypoint,
        f"/{api_name}/contexts/EntryPoint.jsonld",
        endpoint="main_entrypoint",
    )
    api.add_resource(
        ItemCollection, f"/{api_name}/<string:path>", endpoint="item_collection"
    )
    api.add_resource(Item, f"/{api_name}/<string:path>/<uuid:id_>", endpoint="item")

    return app
