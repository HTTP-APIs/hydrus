"""Main route for the applciation."""

# Write code for views and API here.
from flask import Flask
from flask_restful import Api, Resource
from data import crud
# import json
# from models import engine
# from sqlalchemy import text


# from flask_cors import CORS, cross_origin

app = Flask(__name__)
api = Api(app)


def set_response_headers(resp, ct="application/json", status_code=200):
    """
    Set the response headers.

    Default : { Content-type:"JSON-LD", status_code:200}
    """
    resp.status_code = status_code
    resp.headers['Content-type'] = ct
    return resp


def hydrafy():
    """To be implemented."""
    pass


class Index(Resource):
    """Class for the EntryPoint."""

    def get(self):
        """Return main entrypoint for the api."""
        # return set_response_headers(jsonify(entrypoint), 'application/ld+json', 200)
        pass


api.add_resource(Index, "/api", endpoint="api")


class Cots(Resource):
    """Handles all operations(GET, POST, PATCH, DELETE) on Commercial Off The Shelves (COTS) spare parts for pico- and nano-satellites."""

    def get(self, id):
        """."""
        return hydrafy(crud.get(id))

    def post(self, id, object_):
        """."""
        return hydrafy(crud.insert(object_))

    def patch(self, id, object_):
        """."""
        return hydrafy(crud.update(id, object_))

    def delete(self, id):
        """."""
        return hydrafy(crud.delete(id))


api.add_resource(Cots, "/api/cots/<string:id>", endpoint="cots")


class Spacecraft(Resource):
    """Handles all operations(GET, POST, PATCH, DELETE) on Spacecrafts."""

    def get(self, id):
        """."""
        pass

    def post(self, id):
        """."""
        pass

    def patch(self, id):
        """."""
        pass

    def delete(self, id):
        """."""
        pass


api.add_resource(Spacecraft, "/api/spacecraft/<string:id>", endpoint="spacecraft")


class Vocab(Resource):
    """Returns the main Hydra vocab."""

    def get(self):
        """."""
        pass


api.add_resource(Vocab, "/api/vocab#", endpoint="vacab")


class Entrypoint(Resource):
    """Returns application main Entrypoint."""

    def get(self):
        """."""
        pass


api.add_resource(Entrypoint, "/api/contexts/EntryPoint.jsonld", endpoint="main_entrypoint")


class SpacecraftContext(Resource):
    """Return SpaceCraft context."""

    def get(self):
        """."""
        pass


api.add_resource(SpacecraftContext, "/api/contexts/SpaceCraft.jsonld", endpoint="spacecraft_context")


class CotsContext(Resource):
    """Return COTS context."""

    def get(self):
        """."""
        pass


api.add_resource(CotsContext, "/api/contexts/Cots.jsonld", endpoint="cots_context")


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=8080)
