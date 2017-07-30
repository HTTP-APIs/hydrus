"""Main route for the applciation."""

import json
from flask import Flask, jsonify, request, abort
from flask_restful import Api, Resource
from hydrus.data.db_models import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from hydrus.hydraspec.doc_writer import HydraDoc
from hydrus.data import crud
from flask_cors import CORS
from contextlib import contextmanager
from flask import appcontext_pushed
from flask import g
from hydrus.metadata.doc_gen import doc_gen     # Needs to be replaced with sample
# from hydrus.hydraspec.doc_writer_sample import api_doc as doc         # Sample doc


@contextmanager
def set_session(application, DB_SESSION):
    """Set the database session for the app. Must be of type <hydrus.hydraspec.doc_writer.HydraDoc>."""
    if not isinstance(DB_SESSION, Session):
        raise TypeError("The API Doc is not of type <sqlalchemy.orm.session.Session>")

    def handler(sender, **kwargs):
        g.dbsession = DB_SESSION
    with appcontext_pushed.connected_to(handler, application):
        yield


@contextmanager
def set_hydrus_server_url(application, server_url):
    """Set the server URL for the app. Must be of type <str>."""
    if not isinstance(server_url, str):
        raise TypeError("The server_url is not of type <str>")

    def handler(sender, **kwargs):
        g.hydrus_server_url = server_url
    with appcontext_pushed.connected_to(handler, application):
        yield


@contextmanager
def set_api_name(application, api_name):
    """Set the server name or EntryPoint for the app. Must be of type <str>."""
    if not isinstance(api_name, str):
        raise TypeError("The api_name is not of type <str>")

    def handler(sender, **kwargs):
        g.api_name = api_name
    with appcontext_pushed.connected_to(handler, application):
        yield


@contextmanager
def set_doc(application, APIDOC):
    """Set the API Documentation for the app. Must be of type <hydrus.hydraspec.doc_writer.HydraDoc>."""
    if not isinstance(APIDOC, HydraDoc):
        raise TypeError("The API Doc is not of type <hydrus.hydraspec.doc_writer.HydraDoc>")

    def handler(sender, **kwargs):
        g.doc = APIDOC
    with appcontext_pushed.connected_to(handler, application):
        yield


def get_doc():
    """Get the server API Documentation."""
    apidoc = getattr(g, 'doc', None)
    if apidoc is None:
        apidoc = doc_gen(get_api_name(), get_hydrus_server_url())
        g.doc = apidoc
    return apidoc


def get_api_name():
    """Get the server API name."""
    api_name = getattr(g, 'api_name', None)
    if api_name is None:
        api_name = "api"
        g.doc = api_name
    return api_name


def get_hydrus_server_url():
    """Get the server URL."""
    hydrus_server_url = getattr(g, 'hydrus_server_url', None)
    if hydrus_server_url is None:
        hydrus_server_url = "http://localhost/"
        g.hydrus_server_url = hydrus_server_url
    return hydrus_server_url


def get_session():
    """Get the Database Session for the server."""
    session = getattr(g, 'dbsession', None)
    if session is None:
        session = sessionmaker(bind=engine)()
        g.dbsession = session
    return session


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
    resp.headers['Link'] = '<' + get_hydrus_server_url() + \
        get_api_name()+'/vocab>; rel="http://www.w3.org/ns/hydra/core#apiDocumentation"'
    return resp


def hydrafy(object_):
    """Add hydra context to objects."""
    object_["@context"] = "/"+get_api_name()+"/contexts/" + object_["@type"] + ".jsonld"
    return object_


def checkEndpoint(method, type_):
    """Check if endpoint and method is supported in the API."""
    for endpoint in get_doc().entrypoint.entrypoint.supportedProperty:
        if type_ == endpoint.name:
            for operation in endpoint.supportedOperation:
                if operation.method == method:
                    return True
    # NOTE: This is checking the EntryPoint object, no need to check class separately.
    # Non collection classes will be present as an endpoint in the Entrypoint object
    return False


def getType(class_type, method):
    """Return the @type of object allowed for POST/PUT."""
    for supportedOp in get_doc().parsed_classes[class_type]["class"].supportedOperation:
        if supportedOp.method == method:
            return supportedOp.expects.replace("vocab:", "")
    # NOTE: Don't use split, if there are more than one substrings with 'vocab:' not everything will be returned.


def checkClassOp(class_type, method):
    """Check if the Class supports the operation."""
    for supportedOp in get_doc().parsed_classes[class_type]["class"].supportedOperation:
        if supportedOp.method == method:
            return True
    return False


class Index(Resource):
    """Class for the EntryPoint."""

    def get(self):
        """Return main entrypoint for the api."""
        return set_response_headers(jsonify(get_doc().entrypoint.get()))


class Vocab(Resource):
    """Vocabulary for Hydra."""

    def get(self):
        """Return the main hydra vocab."""
        return set_response_headers(jsonify(get_doc().generate()))


class Entrypoint(Resource):
    """Hydra EntryPoint."""

    def get(self):
        """Return application main Entrypoint."""
        response = {"@context": get_doc().entrypoint.context.generate()}
        return set_response_headers(jsonify(response))


class Item(Resource):
    """Handles all operations(GET, POST, PATCH, DELETE) on Items (item can be anything depending upon the vocabulary)."""

    def get(self, id_, type_):
        """GET object with id = id_ from the database."""
        class_type = get_doc().collections[type_]["collection"].class_.title

        if checkClassOp(class_type, "GET"):

            response = crud.get(id_, class_type, api_name=get_api_name(), session=get_session())

            if len(response.keys()) == 1:
                status_code = int(list(response.keys())[0])
                return set_response_headers(jsonify(response), status_code=status_code)

            else:
                response["@id"] = '/'+get_api_name()+'/'+type_+'/'+str(id_)
                return set_response_headers(jsonify(hydrafy(response)))

        abort(405)

    def post(self, id_, type_):
        """Update object of type<type_> at ID<id_> with new object_ using HTTP POST."""
        class_type = get_doc().collections[type_]["collection"].class_.title

        if checkClassOp(class_type, "POST"):

            object_ = json.loads(request.data.decode('utf-8'))
            obj_type = getType(class_type, "POST")

            if validObject(object_):

                if object_["@type"] == obj_type:
                    response = crud.update(object_=object_, id_=id_, type_=object_["@type"], session=get_session(), api_name=get_api_name())
                    object_id = response[list(response.keys())[0]].split("=")[1]
                    headers_ = [{"Location": get_hydrus_server_url()+get_api_name()+"/"+type_+"/"+str(object_id)}]
                    status_code = int(list(response.keys())[0])
                    return set_response_headers(jsonify(response), headers=headers_, status_code=status_code)

            return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

        abort(405)

    def put(self, id_, type_):
        """Add new object_ optional <id_> parameter using HTTP PUT."""
        class_type = get_doc().collections[type_]["collection"].class_.title

        if checkClassOp(class_type, "PUT"):

            object_ = json.loads(request.data.decode('utf-8'))
            obj_type = getType(class_type, "PUT")

            if validObject(object_):

                if object_["@type"] == obj_type:
                    response = crud.insert(object_=object_, id_=id_, session=get_session())
                    headers_ = [{"Location": get_hydrus_server_url()+get_api_name()+"/"+type_+"/"+str(id_)}]
                    status_code = int(list(response.keys())[0])
                    return set_response_headers(jsonify(response), headers=headers_, status_code=status_code)

            return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

        abort(405)

    def delete(self, id_, type_):
        """Delete object with id=id_ from database."""
        class_type = get_doc().collections[type_]["collection"].class_.title

        if checkClassOp(class_type, "DELETE"):
            response = crud.delete(id_, class_type, session=get_session())
            status_code = int(list(response.keys())[0])
            return set_response_headers(jsonify(response), status_code=status_code)

        abort(405)


class ItemCollection(Resource):
    """Handle operation related to ItemCollection (a collection of items)."""

    def get(self, type_):
        """Retrieve a collection of items from the database."""
        if checkEndpoint("GET", type_):
            # Collections
            if type_ in get_doc().collections:

                collection = get_doc().collections[type_]["collection"]
                response = crud.get_collection(get_api_name(), collection.class_.title, session=get_session())

                if "members" in response:
                    return set_response_headers(jsonify(hydrafy(response)))

                else:
                    status_code = int(list(response.keys())[0])
                    response = crud.get_collection(get_api_name(), type_, session=get_session())
                    return set_response_headers(jsonify(response), status_code=status_code)

            # Non Collection classes
            elif type_ in get_doc().parsed_classes and type_+"Collection" not in get_doc().collections:
                response = crud.get_single(type_, api_name=get_api_name(), session=get_session())

                if len(response.keys()) == 1:
                    status_code = int(list(response.keys())[0])
                    return set_response_headers(jsonify(response), status_code=status_code)

                else:
                    return set_response_headers(jsonify(hydrafy(response)))

        abort(405)

    def put(self, type_):
        """Add item to ItemCollection."""
        if checkEndpoint("PUT", type_):
            object_ = json.loads(request.data.decode('utf-8'))
            # Collections
            if type_ in get_doc().collections:
                collection = get_doc().collections[type_]["collection"]
                obj_type = collection.class_.title

                if validObject(object_):

                    if object_["@type"] == obj_type:
                        response = crud.insert(object_=object_, session=get_session())
                        object_id = response[list(response.keys())[0]].split('=')[1]
                        headers_ = [{"Location": get_hydrus_server_url()+get_api_name()+"/"+type_+"/"+str(object_id)}]
                        status_code = int(list(response.keys())[0])
                        return set_response_headers(jsonify(response), headers=headers_, status_code=status_code)

                return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)
            # Non Collection classes
            elif type_ in get_doc().parsed_classes and type_+"Collection" not in get_doc().collections:
                obj_type = getType(type_, "PUT")

                if object_["@type"] == obj_type:

                    if validObject(object_):
                        response = crud.insert_single(object_=object_, session=get_session())
                        headers_ = [{"Location": get_hydrus_server_url()+get_api_name()+"/"+type_+"/"}]
                        status_code = int(list(response.keys())[0])
                        return set_response_headers(jsonify(response), headers=headers_, status_code=status_code)

                return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

        abort(405)

    def post(self, type_):
        """Update Non Collection class item."""
        if checkEndpoint("POST", type_):
            object_ = json.loads(request.data.decode('utf-8'))

            if type_ in get_doc().parsed_classes and type_+"Collection" not in get_doc().collections:
                obj_type = getType(type_, "POST")

                if validObject(object_):

                    if object_["@type"] == obj_type:
                        response = crud.update_single(object_=object_, session=get_session(), api_name=get_api_name())
                        headers_ = [{"Location": get_hydrus_server_url()+get_api_name()+"/"+type_+"/"}]
                        status_code = int(list(response.keys())[0])
                        return set_response_headers(jsonify(response), headers=headers_, status_code=status_code)

                return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

        abort(405)

    def delete(self, type_):
        """Delete a non Collection class item."""
        if checkEndpoint("DELETE", type_):
            # No Delete Operation for collections
            if type_ in get_doc().parsed_classes and type_+"Collection" not in get_doc().collections:
                response = crud.delete_single(type_, session=get_session())
                status_code = int(list(response.keys())[0])
                return set_response_headers(jsonify(response), status_code=status_code)

        abort(405)


class Contexts(Resource):
    """Dynamically genereated contexts."""

    def get(self, category):
        """Return the context for the specified class."""
        if "Collection" in category:

            if category in get_doc().collections:
                response = {"@context": get_doc().collections[category]["context"].generate()}
                return set_response_headers(jsonify(response))

            else:
                response = {404: "NOT FOUND"}
                return set_response_headers(jsonify(response), status_code=404)

        else:

            if category in get_doc().parsed_classes:
                response = {"@context": get_doc().parsed_classes[category]["context"].generate()}
                return set_response_headers(jsonify(response))

            else:
                response = {404: "NOT FOUND"}
                return set_response_headers(jsonify(response), status_code=404)


def app_factory(API_NAME="api"):
    """Create an app object."""
    app = Flask(__name__)

    CORS(app)
    app.url_map.strict_slashes = False
    api = Api(app)

    api.add_resource(Index, "/"+API_NAME+"/", endpoint="api")
    api.add_resource(Vocab, "/"+API_NAME+"/vocab", endpoint="vocab")
    api.add_resource(Contexts, "/"+API_NAME+"/contexts/<string:category>.jsonld", endpoint="contexts")
    api.add_resource(Entrypoint, "/"+API_NAME+"/contexts/EntryPoint.jsonld", endpoint="main_entrypoint")
    api.add_resource(ItemCollection, "/"+API_NAME+"/<string:type_>", endpoint="item_collection")
    api.add_resource(Item, "/"+API_NAME+"/<string:type_>/<int:id_>", endpoint="item")

    return app


if __name__ == "__main__":

    app = app_factory("api")
    app.run(host='127.0.0.1', debug=True, port=8080)
