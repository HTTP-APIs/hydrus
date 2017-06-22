"""Main route for the applciation."""

from flask import Flask, jsonify, request
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


def validObject(object_):
    """Check if the data passed in POST is of valid format or not."""
    if "name" in object_:
        if "@type" in object_:
            if "object" in object_:
                return True
    return False


def set_response_headers(resp, ct="application/json", status_code=200):
    """
    Set the response headers.

    Default : { Content-type:"JSON-LD", status_code:200}
    """
    resp.status_code = status_code
    resp.headers['Content-type'] = ct
    return resp


def get_supported_properties(parsed_classes, category, vocab):
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

            except KeyError:
                prop = (obj_["property"].rsplit('/', 1)[-1], obj_["property"])

            if prop not in supported_props:
                supported_props.append(prop)
        return supported_props
    return {404: "Not Found"}


def gen_context(parsed_classes, server_url, category):
    """Generate dynamic contexts for every item."""
    SERVER_URL = server_url

    context_template = {
        "@context": {
            "hydra": "http://www.w3.org/ns/hydra/core#",
            "vocab": SERVER_URL + "api/vocab#",
            "name": "http://schema.org/name",
            "subsystems": "http://ontology.projectchronos.eu/subsystems?format=jsonld",
            }
    }
    # Get supported properties
    supported_props = get_supported_properties(parsed_classes, category, vocab)
    if type(supported_props) is list:
        for title, value in supported_props:
            context_template["@context"][title] = value
        return context_template
    return supported_props


def gen_collection_context(parsed_classes, server_url, category):
    """Generate context for Collection objects."""
    validCategory = False
    class_name = category.replace("Collection", "")
    for obj in parsed_classes:
        if obj["title"] == class_name:
            validCategory = True
            break

    if validCategory:
        SERVER_URL = server_url
        COLLECTION_TYPE = class_name
        template = {
            "@context": {
                "hydra": "http://www.w3.org/ns/hydra/core#",
                "vocab": SERVER_URL + "api/vocab#",
                COLLECTION_TYPE+"Collection": "vocab:%sCollection" % (COLLECTION_TYPE,),
                COLLECTION_TYPE: "vocab:" + COLLECTION_TYPE,
                "members": "http://www.w3.org/ns/hydra/core#member"
                }
        }

        return template
    return {404: "Not Found"}


def hydrafy(object_, collection=False):
    """Add hydra context to objects."""
    if collection:
        object_["@context"] = "api/contexts/"+object_["@type"]+".jsonld"
    else:
        object_["@context"] = "api/contexts/"+object_["@type"]+".jsonld"
        data = object_.pop("object")
        for key in data:
            object_[key] = data[key]
    return object_


class Index(Resource):
    """Class for the EntryPoint."""

    def get(self):
        """Return main entrypoint for the api."""
        return set_response_headers(jsonify(entrypoint))


api.add_resource(Index, "/api/", endpoint="api")


class Item(Resource):
    """Handles all operations(GET, POST, PATCH, DELETE) on Items (item can be anything depending upon the vocabulary)."""

    def get(self, id_, type_):
        """GET object with id = id_ from the database."""
        response = crud.get(id_, type_)
        if "object" in response:
            return set_response_headers(jsonify(hydrafy(response)))
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
        response = crud.delete(id_, type_)
        status_code = int(list(response.keys())[0])
        return set_response_headers(jsonify(response), status_code=status_code)


api.add_resource(Item, "/api/<string:type_>/<int:id_>", endpoint="item")


class ItemCollection(Resource):
    """Handle operation related to ItemCollection (a collection of items)."""

    def get(self, type_):
        """Retrieve a collection of items from the database."""
        response = crud.get_collection(type_)
        if "members" in response:
            return set_response_headers(jsonify(hydrafy(response, collection=True)))
        else:
            status_code = int(list(response.keys())[0])
            return set_response_headers(jsonify(response), status_code=status_code)


# Needs to be added manually.
api.add_resource(ItemCollection, "/api/<string:type_>/",
                 endpoint="item_collection/")


class Contexts(Resource):
    """Dynamically genereated contexts."""

    def get(self, category):
        """Return the context for the specified class."""
        if "Collection" in category:
            return gen_collection_context(parsed_classes, "http://hydrus.com/", category)
        else:
            return gen_context(parsed_classes, "http://hydrus.com/", category)


api.add_resource(Contexts, "/api/contexts/<string:category>.jsonld", endpoint="contexts")


class Vocab(Resource):
    """Vocabulary for Hydra."""

    def get(self):
        """Return the main hydra vocab."""
        return set_response_headers(jsonify(vocab))


api.add_resource(Vocab, "/api/vocab", endpoint="vocab")


class Entrypoint(Resource):
    """Hydra EntryPoint."""

    def get(self):
        """Return application main Entrypoint."""
        return set_response_headers(jsonify(entrypoint_context))


api.add_resource(Entrypoint, "/api/contexts/EntryPoint.jsonld",
                 endpoint="main_entrypoint")

# Cots context added dynamically

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=8080)
