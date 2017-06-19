"""Main route for the applciation."""

from flask import Flask, jsonify
from flask_restful import Api, Resource
from hydrus.data import crud
# import json
from hydrus.metadata.vocab import vocab
from hydrus.hydraspec.contexts.entrypoint import entrypoint_context
from hydrus.metadata.entrypoint import entrypoint
from hydrus.hydraspec.contexts.cots import cots_context


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


def hydrafy(object_):
    """Adds hydra context to objects."""
    object_["@context"] = cots_context["@context"]
    return object_




class Index(Resource):
    """Class for the EntryPoint."""

    def get(self):
        """Return main entrypoint for the api."""
        return set_response_headers(jsonify(entrypoint), 'application/ld+json', 200)


api.add_resource(Index, "/api", endpoint="api")




class Cots(Resource):
    """Handles all operations(GET, POST, PATCH, DELETE) on Commercial Off The Shelves (COTS) spare parts for pico- and nano-satellites."""

    def get(self, id_):
        """GET object with id = id_ from the database."""
        return set_response_headers(jsonify(hydrafy(crud.get(id_))))

    def post(self, id_, object_):
        """Add object_ to database with optional id_ parameter (The id where the object needs to be inserted).
        If object with id_ already exists update it."""
        insert_id = crud.insert(object_, id_)
        resp = {204: "Object with ID:%s succesfully inserted." % (insert_id)}
        return resp

    def patch(self, id_, object_):
        """Update object at id=id_ with object_ in database."""
        resp = crud.update(id_, object_)
        return resp

    def delete(self, id_):
        """Delete object with id=id_ from database."""
        resp = crud.delete(id_)
        return resp

api.add_resource(Cots, "/api/cots/<string:id>", endpoint="cots")




class Vocab(Resource):

    def get(self):
        """Return the main hydra vocab."""
        return set_response_headers(jsonify(vocab), 'application/ld+json', 200)


api.add_resource(Vocab, "/api/vocab", endpoint="vocab")




class Entrypoint(Resource):

    def get(self):
        """Return application main Entrypoint."""
        return set_response_headers(jsonify(entrypoint_context), 'application/ld+json', 200)


api.add_resource(Entrypoint, "/api/contexts/EntryPoint.jsonld",
                 endpoint="main_entrypoint")




class CotsContext(Resource):

    def get(self):
        """Return COTS context."""
        return set_response_headers(jsonify(cots_context), 'application/ld+json', 200)


api.add_resource(CotsContext, "/api/contexts/Cots.jsonld",
                 endpoint="cots_context")





if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
