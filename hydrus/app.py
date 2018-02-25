"""Main route for the applciation."""

import json
from flask import Flask, jsonify, request, abort
from flask_restful import Api, Resource
from flask_cors import CORS

from hydrus.data import crud
from hydrus.data.user import check_authorization
from hydrus.utils import get_session, get_doc, get_api_name, get_hydrus_server_url, get_authentication

import pdb


def valid_object(object_):
    """Check if the data passed in POST is of valid format or not."""
    if "@type" in object_:
        return True
    return False


def failed_authentication():
    """Return failed authentication object."""
    message = {401: "Need credentials to authenticate"}
    response = set_response_headers(jsonify(message), status_code=401,
                                    headers=[{'WWW-Authenticate': 'Basic realm="Login Required"'}])
    return response


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


def check_endpoint(method, type_):
    """Check if endpoint and method is supported in the API."""
    for endpoint in get_doc().entrypoint.entrypoint.supportedProperty:
        if type_ == endpoint.name:
            for operation in endpoint.supportedOperation:
                if operation.method == method:
                    return True
    return False


def get_type(class_type, method):
    """Return the @type of object allowed for POST/PUT."""
    for supportedOp in get_doc().parsed_classes[class_type]["class"].supportedOperation:
        if supportedOp.method == method:
            return supportedOp.expects.replace("vocab:", "")
    # NOTE: Don't use split, if there are more than one substrings with 'vocab:' not everything will be returned.


def check_class_op(class_type, method):
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


class EntryPoint(Resource):
    """Hydra EntryPoint."""

    def get(self):
        """Return application main Entrypoint."""
        response = {"@context": get_doc().entrypoint.context.generate()}
        return set_response_headers(jsonify(response))


class Item(Resource):
    """Handles all operations(GET, POST, PATCH, DELETE) on Items (item can be anything depending upon the vocabulary)."""

    def get(self, id_, type_):
        """GET object with id = id_ from the database."""
        if get_authentication():
            if request.authorization is None:
                return failed_authentication()
            else:
                auth = check_authorization(request, get_session())
                if auth is False:
                    return failed_authentication()

        class_type = get_doc().collections[type_]["collection"].class_.title

        if check_class_op(class_type, "GET"):

            try:
                response = crud.get(id_, class_type, api_name=get_api_name(), session=get_session())
                return set_response_headers(jsonify(hydrafy(response)))

            except Exception as e:
                status_code, message = e.get_HTTP()
                return set_response_headers(jsonify(message), status_code=status_code)

        abort(405)

    def post(self, id_, type_):
        """Update object of type<type_> at ID<id_> with new object_ using HTTP POST."""
        if get_authentication():
            if request.authorization is None:
                return failed_authentication()
            else:
                auth = check_authorization(request, get_session())
                if auth is False:
                    return failed_authentication()

        class_type = get_doc().collections[type_]["collection"].class_.title

        if check_class_op(class_type, "POST"):

            object_ = json.loads(request.data.decode('utf-8'))
            obj_type = get_type(class_type, "POST")

            if valid_object(object_):

                if object_["@type"] == obj_type:
                    try:
                        object_id = crud.update(object_=object_, id_=id_, type_=object_["@type"], session=get_session(), api_name=get_api_name())
                        headers_ = [{"Location": get_hydrus_server_url()+get_api_name()+"/"+type_+"/"+str(object_id)}]
                        response = {"message": "Object with ID %s successfully updated" % (object_id)}
                        return set_response_headers(jsonify(response), headers=headers_)

                    except Exception as e:
                        status_code, message = e.get_HTTP()
                        return set_response_headers(jsonify(message), status_code=status_code)

            return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

        abort(405)

    def put(self, id_, type_):
        """Add new object_ optional <id_> parameter using HTTP PUT."""
        if get_authentication():
            if request.authorization is None:
                return failed_authentication()
            else:
                auth = check_authorization(request, get_session())
                if auth is False:
                    return failed_authentication()

        class_type = get_doc().collections[type_]["collection"].class_.title

        if check_class_op(class_type, "PUT"):

            object_ = json.loads(request.data.decode('utf-8'))
            obj_type = get_type(class_type, "PUT")

            if valid_object(object_):

                if object_["@type"] == obj_type:
                    try:
                        object_id = crud.insert(object_=object_, id_=id_, session=get_session())
                        headers_ = [{"Location": get_hydrus_server_url()+get_api_name()+"/"+type_+"/"+str(object_id)}]
                        response = {"message": "Object with ID %s successfully added" % (object_id)}
                        return set_response_headers(jsonify(response), headers=headers_, status_code=201)

                    except Exception as e:
                        status_code, message = e.get_HTTP()
                        return set_response_headers(jsonify(message), status_code=status_code)

            return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

        abort(405)

    def delete(self, id_, type_):
        """Delete object with id=id_ from database."""
        if get_authentication():
            if request.authorization is None:
                return failed_authentication()
            else:
                auth = check_authorization(request, get_session())
                if auth is False:
                    return failed_authentication()

        class_type = get_doc().collections[type_]["collection"].class_.title

        if check_class_op(class_type, "DELETE"):
            try:
                crud.delete(id_, class_type, session=get_session())
                response = {"message": "Object with ID %s successfully deleted" % (id_)}
                return set_response_headers(jsonify(response))

            except Exception as e:
                status_code, message = e.get_HTTP()
                return set_response_headers(jsonify(message), status_code=status_code)

        abort(405)


class ItemCollection(Resource):
    """Handle operation related to ItemCollection (a collection of items)."""

    def get(self, type_):
        """Retrieve a collection of items from the database."""
        if get_authentication():
            if request.authorization is None:
                return failed_authentication()
            else:
                auth = check_authorization(request, get_session())
                if auth is False:
                    return failed_authentication()

        if check_endpoint("GET", type_):
            # Collections
            if type_ in get_doc().collections:

                collection = get_doc().collections[type_]["collection"]
                try:
                    response = crud.get_collection(get_api_name(), collection.class_.title, session=get_session())
                    return set_response_headers(jsonify(hydrafy(response)))

                except Exception as e:
                    status_code, message = e.get_HTTP()
                    return set_response_headers(jsonify(message), status_code=status_code)

            # Non Collection classes
            elif type_ in get_doc().parsed_classes and type_+"Collection" not in get_doc().collections:
                try:
                    response = crud.get_single(type_, api_name=get_api_name(), session=get_session())
                    return set_response_headers(jsonify(hydrafy(response)))

                except Exception as e:
                    status_code, message = e.get_HTTP()
                    return set_response_headers(jsonify(message), status_code=status_code)

        abort(405)

    def put(self, type_):
        """Add item to ItemCollection."""
        if get_authentication():
            if request.authorization is None:
                return failed_authentication()
            else:
                auth = check_authorization(request, get_session())
                if auth is False:
                    return failed_authentication()

        if check_endpoint("PUT", type_):
            object_ = json.loads(request.data.decode('utf-8'))

            # Collections
            if type_ in get_doc().collections:

                collection = get_doc().collections[type_]["collection"]
                obj_type = collection.class_.title

                if valid_object(object_):

                    if object_["@type"] == obj_type:
                        try:
                            object_id = crud.insert(object_=object_, session=get_session())
                            headers_ = [{"Location": get_hydrus_server_url()+get_api_name()+"/"+type_+"/"+str(object_id)}]
                            response = {"message": "Object with ID %s successfully deleted" % (object_id)}
                            return set_response_headers(jsonify(response), headers=headers_, status_code=201)
                        except Exception as e:
                            status_code, message = e.get_HTTP()
                            return set_response_headers(jsonify(message), status_code=status_code)

                return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

            # Non Collection classes
            elif type_ in get_doc().parsed_classes and type_+"Collection" not in get_doc().collections:
                obj_type = get_type(type_, "PUT")

                if object_["@type"] == obj_type:

                    if valid_object(object_):
                        try:
                            object_id = crud.insert(object_=object_, session=get_session())
                            headers_ = [{"Location": get_hydrus_server_url()+get_api_name()+"/"+type_+"/"}]
                            response = {"message": "Object successfully added"}
                            return set_response_headers(jsonify(response), headers=headers_, status_code=201)
                        except Exception as e:
                            status_code, message = e.get_HTTP()
                            return set_response_headers(jsonify(message), status_code=status_code)

                return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

        abort(405)

    def post(self, type_):
        """Update Non Collection class item."""
        if get_authentication():
            if request.authorization is None:
                return failed_authentication()
            else:
                auth = check_authorization(request, get_session())
                if auth is False:
                    return failed_authentication()

        if check_endpoint("POST", type_):
            object_ = json.loads(request.data.decode('utf-8'))

            if type_ in get_doc().parsed_classes and type_+"Collection" not in get_doc().collections:
                obj_type = get_type(type_, "POST")

                if valid_object(object_):

                    if object_["@type"] == obj_type:
                        # try:
                            crud.update_single(object_=object_, session=get_session(), api_name=get_api_name())
                            headers_ = [{"Location": get_hydrus_server_url()+get_api_name()+"/"+type_+"/"}]
                            response = {"message": "Object successfully updated"}
                            return set_response_headers(jsonify(response), headers=headers_)
                        # except Exception as e:
                        #     status_code, message = e.get_HTTP()
                        #     return set_response_headers(jsonify(message), status_code=status_code)

                return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

        abort(405)

    def delete(self, type_):
        """Delete a non Collection class item."""
        if get_authentication():
            if request.authorization is None:
                return failed_authentication()
            else:
                auth = check_authorization(request, get_session())
                if auth is False:
                    return failed_authentication()

        if check_endpoint("DELETE", type_):
            # No Delete Operation for collections
            if type_ in get_doc().parsed_classes and type_+"Collection" not in get_doc().collections:
                try:
                    crud.delete_single(type_, session=get_session())
                    response = {"message": "Object successfully deleted"}
                    return set_response_headers(jsonify(response))
                except Exception as e:
                    status_code, message = e.get_HTTP()
                    return set_response_headers(jsonify(message), status_code=status_code)
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
    api.add_resource(EntryPoint, "/" + API_NAME + "/contexts/EntryPoint.jsonld", endpoint="main_entrypoint")
    api.add_resource(ItemCollection, "/"+API_NAME+"/<string:type_>", endpoint="item_collection")
    api.add_resource(Item, "/"+API_NAME+"/<string:type_>/<int:id_>", endpoint="item")

    return app


if __name__ == "__main__":

    app = app_factory("api")
    app.run(host='127.0.0.1', debug=True, port=8080)
