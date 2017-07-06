"""Main route for the applciation."""

import os
import json
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from hydrus.metadata.spacecraft_parsed_classes import parsed_classes
from hydrus.hydraspec.vocab_generator import gen_vocab
from hydrus.hydraspec.entrypoint_generator import gen_entrypoint
from hydrus.hydraspec.entrypoint_context_generator import gen_entrypoint_context
from hydrus.data import crud
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
api = Api(app)

global SERVER_URL, SEMANTIC_REF_NAME, SEMANTIC_REF_URL, PARSED_CLASSES
SERVER_URL = os.environ.get("HYDRUS_SERVER_URL", "localhost/")
SEMANTIC_REF_NAME = "subsystems"
SEMANTIC_REF_URL = "http://ontology.projectchronos.eu/subsystems"
PARSED_CLASSES = parsed_classes

## Save data in memory to improve performance
global VOCAB, ENTRYPOINT, ENTRYPOINT_CONTEXT
VOCAB = gen_vocab(PARSED_CLASSES, SERVER_URL, SEMANTIC_REF_NAME, SEMANTIC_REF_URL)
ENTRYPOINT = gen_entrypoint(SERVER_URL, PARSED_CLASSES)
ENTRYPOINT_CONTEXT = gen_entrypoint_context(SERVER_URL, parsed_classes)

def validObject(object_):
    """Check if the data passed in POST is of valid format or not."""
    if "name" in object_:
        if "@type" in object_:
            if "object" in object_:
                return True
    return False


def set_response_headers(resp, ct="application/ld+json", status_code=200):
    # NOTE: This isn't needed, flask automatically does this when you return a Python dict
    #       Just use : "return response_dict, status_code"
    """
    Set the response headers.

    Default : { Content-type:"JSON-LD", status_code:200}
    """
    resp.status_code = status_code
    resp.headers['Content-type'] = ct
    resp.headers['Link'] = '<'+SERVER_URL+'api/vocab>; rel="http://www.w3.org/ns/hydra/core#apiDocumentation"'
    return resp


def get_supported_properties(parsed_classes, category, vocab):
    """Filter supported properties with their title (title, property) for a specific class from the parsed classes."""
    obj = None
    for object_ in parsed_classes:
        if object_["title"] == category:
            obj = object_
    # print(obj, category)

    supported_props = []
    if obj is not None:
        # Get object class and title
        supported_props.append((obj["title"], obj["@id"]))
        # Get supported properties
        for obj_ in obj["supportedProperty"]:
            try:
                prop = (obj_["title"], obj_["property"])

            except KeyError:
                prop = (obj_["property"].split("subsystems:")[-1], obj_["property"])

            if prop not in supported_props:
                supported_props.append(prop)
    return supported_props


def gen_context(parsed_classes, server_url, category):
    """Generate dynamic contexts for every item."""
    SERVER_URL = server_url

    context_template = {
        "@context":{
        "name": "http://schema.org/name",
        "object": "http://schema.org/object",
        "hydra": "http://www.w3.org/ns/hydra/core#",
        "vocab": SERVER_URL + "api/vocab#",
        }
    }

    # Get supported properties
    supported_props = get_supported_properties(parsed_classes, category, vocab)
    for title, value in supported_props:
        context_template["@context"][title] = value

    return context_template

def gen_collection_context(server_url, type_ , semantic_ref_url):
    """Generate context for Collection objects."""
    SEMANTIC_REF_URL = semantic_ref_url
    SERVER_URL = server_url
    COLLECTION_TYPE = type_.split("Collection")[0]

    template = {
    "@context":{
    "hydra": "http://www.w3.org/ns/hydra/core#",
    "vocab": SERVER_URL + "api/vocab#",
    COLLECTION_TYPE+"Collection": "vocab:%sCollection" %(COLLECTION_TYPE,),
    COLLECTION_TYPE: SEMANTIC_REF_URL.split("?")[0]+COLLECTION_TYPE,

    "members": "http://www.w3.org/ns/hydra/core#member"
    }
  }

    return template

def hydrafy(parsed_classes, object_, collection = False):
    """Add hydra context to objects."""
    if collection:
        object_["@context"] = "/api/contexts/"+object_["@type"]+".jsonld"
    else:
        object_["@context"] = "/api/contexts/"+object_["@type"]+".jsonld"
    return object_


class Index(Resource):
    """Class for the EntryPoint."""

    def get(self):
        """Return main entrypoint for the api."""
        return set_response_headers(jsonify(ENTRYPOINT))


api.add_resource(Index, "/api", endpoint="api")


class Item(Resource):
    """Handles all operations(GET, POST, PATCH, DELETE) on Items (item can be anything depending upon the vocabulary)."""

    def get(self, id_, type_):
        """GET object with id = id_ from the database."""
        response = crud.get(id_, type_)
        if "object" in response:
            return set_response_headers(jsonify(hydrafy(PARSED_CLASSES, response)))
        else:
            status_code = int(list(response.keys())[0])
            return set_response_headers(jsonify(response), status_code=status_code)

    def post(self, id_, type_):
        """Add object_ to database with optional id_ parameter (The id where the object needs to be inserted)."""
        object_ = json.loads(request.data.decode('utf-8'))
        if validObject(object_):
            response = crud.insert(object_=object_, id_=id_)
            status_code = int(list(response.keys())[0])
            return set_response_headers(jsonify(response), status_code=status_code)
        else:
            return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

    def put(self, id_, type_):
        """Update object at id=id_ with object_ in database."""
        object_ = json.loads(request.data.decode('utf-8'))
        if validObject(object_):
            response = crud.update(object_=object_, id_=id_, type_=type_)
            status_code = int(list(response.keys())[0])
            return set_response_headers(jsonify(response), status_code=status_code)
        else:
            return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

    def delete(self, id_, type_):
        """Delete object with id=id_ from database."""
        resp = crud.delete(id_, type_)
        return set_response_headers(jsonify(resp))


# Needs to be changed manually
api.add_resource(Item, "/api/<string:type_>/<int:id_>", endpoint="item")


class ItemCollection(Resource):
    """Handle operation related to ItemCollection (a collection of items)."""

    def get(self, type_):
        """Retrieve a collection of items from the database."""
        response = crud.get_collection(type_)
        if "members" in response:
            return set_response_headers(jsonify(hydrafy(PARSED_CLASSES, response, collection=True)))
        else:
            status_code = int(list(response.keys())[0])
            return set_response_headers(jsonify(response), status_code=status_code)


# Needs to be added manually.
api.add_resource(ItemCollection, "/api/<string:type_>",
                 endpoint="item_collection")

class Contexts(Resource):
    """Dynamically genereated contexts."""

    def get(self, category):
        """Return the context for the specified class."""
        if "Collection" in category:
            response = gen_collection_context(SERVER_URL, category, "http://ontology.projectchronos.eu/subsystems/")
            if "@context" in response:
                return set_response_headers(jsonify(response))
            else:
                status_code = int(list(response.keys())[0])
                return set_response_headers(jsonify(response), status_code=status_code)
        else:
            response = gen_context(PARSED_CLASSES, SERVER_URL, category)
            if "@context" in response:
                return set_response_headers(jsonify(response))
            else:
                status_code = int(list(response.keys())[0])
                return set_response_headers(jsonify(response), status_code=status_code)


api.add_resource(Contexts, "/api/contexts/<string:category>.jsonld", endpoint="contexts")



class Vocab(Resource):
    """Vocabulary for Hydra."""

    def get(self):
        """Return the main hydra vocab."""
        return set_response_headers(jsonify(VOCAB))


api.add_resource(Vocab, "/api/vocab", endpoint="vocab")


class Entrypoint(Resource):
    """Hydra EntryPoint."""

    def get(self):
        """Return application main Entrypoint."""
        return set_response_headers(jsonify(ENTRYPOINT_CONTEXT))


api.add_resource(Entrypoint, "/api/contexts/EntryPoint.jsonld",
                 endpoint="main_entrypoint")

# Cots context added dynamically

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=8080)
