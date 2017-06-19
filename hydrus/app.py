"""Main route for the applciation."""

from flask import Flask, jsonify
from flask_restful import Api, Resource
from hydrus.data import crud
import json
from hydrus.metadata.vocab import vocab
from hydrus.hydraspec.contexts.entrypoint import entrypoint_context
from hydrus.metadata.entrypoint import entrypoint
from hydrus.metadata.subsystem_parsed_classes import parsed_classes


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

def get_supported_properties(category, vocab):
    """Filter supported properties with their title (title, property) for a specific class from the parsed classes."""
    obj = None
    for object_ in parsed_classes:
        if object_["title"] == category:
            obj = object_

    supported_props = []
    if obj is not None:
        # Get object class and title
        supported_props.append((obj["title"], obj["@id"]))
        # Get supported properties
        for obj_ in obj["supportedProperty"]:
            try:
                prop = (obj_["title"], obj_["property"])
                if prop not in supported_props:
                    supported_props.append(prop)
            except:
                # If title key is not present take the last part of url as title
                prop = (obj_["property"].rsplit('/', 1)[-1], obj_["property"])
                if prop not in supported_props:
                    supported_props.append(prop)

    return supported_props


def gen_context(server_url, object_):
    """Generate dynamic contexts for every item."""
    SERVER_URL = server_url

    context_template = {
    "hydra": "http://www.w3.org/ns/hydra/core#",
    "vocab": SERVER_URL+ "api/vocab#",
    }


    object_category = object_["object"]["category"]
    # Get supported properties
    supported_props = get_supported_properties(object_category, vocab)
    for title, value in supported_props:
        context_template[title] = value

    return context_template



def hydrafy(object_):
    """Adds hydra context to objects."""
    context = gen_context("http://hydrus.com/", object_)
    object_["@context"] = context
    return object_




class Index(Resource):
    """Class for the EntryPoint."""

    def get(self):
        """Return main entrypoint for the api."""
        return set_response_headers(jsonify(entrypoint))


api.add_resource(Index, "/api", endpoint="api")




class Item(Resource):
    """Handles all operations(GET, POST, PATCH, DELETE) on Items (item can be anything depending upon the vocabulary)."""

    def get(self, id_):
        """GET object with id = id_ from the database."""
        obj = crud.get(id_)
        if 404 not in obj.keys():
            return set_response_headers(jsonify(hydrafy(obj)))
        else:
            return set_response_headers(jsonify(obj))

    def post(self, id_, object_):
        """Add object_ to database with optional id_ parameter (The id where the object needs to be inserted).
        If object with id_ already exists update it."""
        insert_id = crud.insert(object_, id_)
        resp = {204: "Object with ID:%s succesfully inserted." % (insert_id)}
        return set_response_headers(jsonify(resp))

    def patch(self, id_, object_):
        """Update object at id=id_ with object_ in database."""
        resp = crud.update(id_, object_)
        return set_response_headers(jsonify(resp))

    def delete(self, id_):
        """Delete object with id=id_ from database."""
        resp = crud.delete(id_)
        return set_response_headers(jsonify(resp))

### Needs to be changed manually
api.add_resource(Cots, "/api/cots/<string:id_>", endpoint="cots")

class ItemCollection(Resource):
    """Handle operation related to ItemCollection (a collection of items)."""

    def get(self):
        """Retrieve a collection of items from the database."""
        # Needs to be discussed.
        pass
        
### Needs to be added manually.
api.add_resource(Cots, "/api/cots", endpoint="cots_collection")


class Vocab(Resource):

    def get(self):
        """Return the main hydra vocab."""
        return set_response_headers(jsonify(vocab))


api.add_resource(Vocab, "/api/vocab", endpoint="vocab")




class Entrypoint(Resource):

    def get(self):
        """Return application main Entrypoint."""
        return set_response_headers(jsonify(entrypoint_context))


api.add_resource(Entrypoint, "/api/contexts/EntryPoint.jsonld",
                 endpoint = "main_entrypoint")

### Cots context added dynamically

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True, port = 8080)
