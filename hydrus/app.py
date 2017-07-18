"""Main route for the applciation."""

import os
import json
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
## Will modify docs for each container using docker.
from hydrus.metadata.doc_gen import doc_gen

from hydrus.data import crud
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.url_map.strict_slashes = False
api = Api(app)

SERVER_URL = os.environ.get("HYDRUS_SERVER_URL", "localhost/")
API_NAME = os.environ.get("API_NAME", "api")
API_DOC = doc_gen(API_NAME, SERVER_URL)
# API_DOC = drone_doc(API_NAME, SERVER_URL)


def validObject(object_):
    """Check if the data passed in POST is of valid format or not."""
    if "@type" in object_:
        return True
    return False


def set_response_headers(resp, ct="application/ld+json", headers=[], status_code=200):
    """Set the response headers."""
    resp.status_code = status_code
    for header in headers:
        resp.headers[list(header.keys())[0]] = header[list(header.keys())[0]]
    resp.headers['Content-type'] = ct
    resp.headers['Link'] = '<' + SERVER_URL + \
        API_NAME+'/vocab>; rel="http://www.w3.org/ns/hydra/core#apiDocumentation"'
    return resp


def hydrafy(object_):
    """Add hydra context to objects."""
    object_["@context"] = "/"+API_NAME+"/contexts/" + object_["@type"] + ".jsonld"
    return object_


class Index(Resource):
    """Class for the EntryPoint."""

    def get(self):
        """Return main entrypoint for the api."""
        return set_response_headers(jsonify(API_DOC.entrypoint.get()))


api.add_resource(Index, "/"+API_NAME+"/", endpoint="api")


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
            response = crud.insert(object_=object_)

            object_id = response[list(response.keys())[0]].split(" ")[3]
            headers_ = [{"Location": SERVER_URL+API_NAME+"/"+type_+"/"+object_id}]
            status_code = int(list(response.keys())[0])

            return set_response_headers(jsonify(response), headers=headers_, status_code=status_code)
        else:
            return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

    def put(self, id_, type_):
        """Update object at id=id_ with object_ in database."""
        object_ = json.loads(request.data.decode('utf-8'))
        if validObject(object_):
            response = crud.update(object_=object_, id_=id_, type_=type_)
            headers_ = [{"Location": SERVER_URL+API_NAME+"/"+type_+"/"+id_}]

            status_code = int(list(response.keys())[0])
            return set_response_headers(jsonify(response), headers=headers_, status_code=status_code)
        else:
            return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

    def delete(self, id_, type_):
        """Delete object with id=id_ from database."""
        resp = crud.delete(id_, type_)
        return set_response_headers(jsonify(resp))


# Needs to be changed manually
api.add_resource(Item, "/"+API_NAME+"/<string:type_>/<int:id_>", endpoint="item")


class ItemCollection(Resource):
    """Handle operation related to ItemCollection (a collection of items)."""

    def get(self, type_):
        """Retrieve a collection of items from the database."""
        if type_ in API_DOC.collections:
            collection = API_DOC.collections[type_]["collection"]
            response = crud.get_collection(API_NAME, collection.class_.title)
            if "members" in response:
                return set_response_headers(jsonify(hydrafy(response)))
            else:
                status_code = int(list(response.keys())[0])
                response = crud.get_collection(API_NAME, type_)

                return set_response_headers(jsonify(response), status_code=status_code)

    def post(self, type_):
        """Add item to ItemCollection."""
        object_ = json.loads(request.data.decode('utf-8'))
        # print(object_)
        # Fix @type from hydra console
        if type_ in API_DOC.collections:
            collection = API_DOC.collections[type_]["collection"]
            type_ = collection.class_.title
            object_["@type"] = type_
        # print(object_)

        if validObject(object_):
            response = crud.insert(object_=object_)
            # print(response)
            object_id = response[list(response.keys())[0]].split(" ")[3]
            headers_ = [{"Location": SERVER_URL+"api/"+type_+"/"+object_id}]
            status_code = int(list(response.keys())[0])

            return set_response_headers(jsonify(response), headers=headers_, status_code=status_code)
        else:
            return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)


# Needs to be added manually.
api.add_resource(ItemCollection, "/"+API_NAME+"/<string:type_>",
                 endpoint="item_collection")


class Contexts(Resource):
    """Dynamically genereated contexts."""

    def get(self, category):
        """Return the context for the specified class."""
        if "Collection" in category:
            if category in API_DOC.collections:
                response = {"@context": API_DOC.collections[category]["context"].generate()}
                return set_response_headers(jsonify(response))
            else:
                response = {404: "NOT FOUND"}
                return set_response_headers(jsonify(response), status_code=404)
        else:
            if category in API_DOC.parsed_classes:
                response = {"@context": API_DOC.parsed_classes[category]["context"].generate()}
                return set_response_headers(jsonify(response))
            else:
                response = {404: "NOT FOUND"}
                return set_response_headers(jsonify(response), status_code=404)


api.add_resource(
    Contexts, "/"+API_NAME+"/contexts/<string:category>.jsonld", endpoint="contexts")


class Vocab(Resource):
    """Vocabulary for Hydra."""

    def get(self):
        """Return the main hydra vocab."""
        return set_response_headers(jsonify(API_DOC.generate()))


api.add_resource(Vocab, "/"+API_NAME+"/vocab", endpoint="vocab")

class Entrypoint(Resource):
    """Hydra EntryPoint."""

    def get(self):
        """Return application main Entrypoint."""
        response = {"@context": API_DOC.entrypoint.context.generate()}
        return set_response_headers(jsonify(response))



api.add_resource(Entrypoint, "/"+API_NAME+"/contexts/EntryPoint.jsonld",
                 endpoint="main_entrypoint")

# Cots context added dynamically

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=8080)
