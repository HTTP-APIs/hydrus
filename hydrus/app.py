"""Main route for the applciation.
    ===============================
    Imports :

    flask.json.jsonify : Turns the JSON output into a Response object with the application/json mimetype
    Ref- http://flask.pocoo.org/docs/0.12/api

    flask.request : The request object used by default in Flask. Remembers the matched endpoint and view arguments.
    Ref - http://flask.pocoo.org/docs/0.12/api

    flask.abort : Raises an HTTPException for the given status code or WSGI application:
    Ref - http://flask.pocoo.org/docs/0.12/api

    flask_restful.Resource : Represents an abstract RESTful resource.
    Ref - http://flask-restful.readthedocs.io/en/latest/api.html


    hydrus.data.crud : Function/Class to perform basic CRUD operations for the server
    hydrus.data.user.check_authorization : Funcion checks if the request object has the correct authorization
    hydrus.utils.get_session : Gets the database session for the server
    hydrus.utils.get_doc : Function which gets the server API documentation
    hydrus.utils.get_api_name : Function which gets the server API name
    hydrus.utils.get_hydrus_server_url : Function the gets the server URL
    hydrus.utils.get_authentication : Function that checks whether API needs to be authenticated or not

"""

import json
from flask import Flask, jsonify, request, abort
from flask_restful import Api, Resource
from flask_cors import CORS

from hydrus.data import crud
from hydrus.data.user import check_authorization
from hydrus.utils import get_session, get_doc, get_api_name, get_hydrus_server_url, get_authentication

from flask.wrappers import Response
from typing import Dict, List, Any, Union
from pprint import pprint


def validObject(object_: Dict[str, Any]) -> bool:
    """
        Check if the Dict passed in POST is of valid format or not.
        (if there's an "@type" key in the dict)

        :param object_ - Object to be checked
    """
    if "@type" in object_:
        return True
    return False


def failed_authentication() -> Response:
    """Return failed authentication object."""
    message = {401: "Need credentials to authenticate"}
    response = set_response_headers(jsonify(message), status_code=401,
                                    headers=[{'WWW-Authenticate': 'Basic realm="Login Required"'}])
    return response


def set_response_headers(resp: Response, ct: str="application/ld+json", headers: List[Dict[str, Any]]=[], status_code: int=200) -> Response:
    """Set the response headers."""
    resp.status_code = status_code
    for header in headers:
        resp.headers[list(header.keys())[0]] = header[list(header.keys())[0]]
    resp.headers['Content-type'] = ct
    resp.headers['Link'] = '<' + get_hydrus_server_url() + \
        get_api_name() + '/vocab>; rel="http://www.w3.org/ns/hydra/core#apiDocumentation"'
    return resp


def hydrafy(object_: Dict[str, Any]) -> Dict[str, Any]:
    """Add hydra context to objects."""
    object_["@context"] = "/" + get_api_name() + "/contexts/" + \
        object_["@type"] + ".jsonld"
    return object_


def checkEndpoint(method: str, type_: str) -> Dict[str, Union[bool, int]]:
    """Check if endpoint and method is supported in the API."""
    status_val = 404
    if type_ == 'vocab':
        return {'method': False, 'status': 405}

    for endpoint in get_doc().entrypoint.entrypoint.supportedProperty:
        if type_ == endpoint.name:
            status_val = 405
            for operation in endpoint.supportedOperation:
                if operation.method == method:
                    status_val = 200
                    return {'method': True, 'status': status_val}
    return {'method': False, 'status': status_val}


def getType(class_type: str, method: str) -> Any:
    """Return the @type of object allowed for POST/PUT."""
    for supportedOp in get_doc().parsed_classes[class_type]["class"].supportedOperation:
        if supportedOp.method == method:
            return supportedOp.expects.replace("vocab:", "")
    # NOTE: Don't use split, if there are more than one substrings with 'vocab:' not everything will be returned.


def checkClassOp(class_type: str, method: str) -> bool:
    """Check if the Class supports the operation."""
    for supportedOp in get_doc().parsed_classes[class_type]["class"].supportedOperation:
        if supportedOp.method == method:
            return True
    return False


class Index(Resource):
    """Class for the EntryPoint."""

    def get(self) -> Response:
        """Return main entrypoint for the api."""
        return set_response_headers(jsonify(get_doc().entrypoint.get()))


class Vocab(Resource):
    """Vocabulary for Hydra."""

    def get(self) -> Response:
        """Return the main hydra vocab."""
        return set_response_headers(jsonify(get_doc().generate()))


class Entrypoint(Resource):
    """Hydra EntryPoint."""

    def get(self) -> Response:
        """Return application main Entrypoint."""
        response = {"@context": get_doc().entrypoint.context.generate()}
        return set_response_headers(jsonify(response))


class Item(Resource):
    """Handles all operations(GET, POST, PATCH, DELETE) on Items (item can be anything depending upon the vocabulary)."""

    def get(self, id_: int, type_: str) -> Response:
        """
        GET object with id = id_ from the database.

        :param id : Item ID
        :param type_ : Item type
        """
        if get_authentication():
            if request.authorization is None:
                return failed_authentication()
            else:
                try:
                    auth = check_authorization(request, get_session())
                    if auth is False:
                        return failed_authentication()
                except Exception as e:
                    status_code, message = e.get_HTTP()  # type: ignore
                    return set_response_headers(jsonify(message), status_code=status_code)

        class_type = get_doc().collections[type_]["collection"].class_.title

        if checkClassOp(class_type, "GET"):
            # Check if class_type supports GET operation
            try:
                # Try getting the Item based on ID and Class type
                response = crud.get(
                    id_, class_type, api_name=get_api_name(), session=get_session())
                return set_response_headers(jsonify(hydrafy(response)))

            except Exception as e:
                status_code, message = e.get_HTTP()  # type: ignore
                return set_response_headers(jsonify(message), status_code=status_code)
        abort(405)

    def post(self, id_: int, type_: str) -> Response:
        """Update object of type<type_> at ID<id_> with new object_ using HTTP POST.

        :param id_ - ID of Item to be updated
        :param type_ - Type(Class name) of Item to be updated
        """
        if get_authentication():
            if request.authorization is None:
                return failed_authentication()
            else:
                try:
                    auth = check_authorization(request, get_session())
                    if auth is False:
                        return failed_authentication()
                except Exception as e:
                    status_code, message = e.get_HTTP()  # type: ignore
                    return set_response_headers(jsonify(message), status_code=status_code)

        class_type = get_doc().collections[type_]["collection"].class_.title

        if checkClassOp(class_type, "POST"):
            # Check if class_type supports POST operation
            object_ = json.loads(request.data.decode('utf-8'))
            obj_type = getType(class_type, "POST")
            # Load new object and type
            if validObject(object_):
                if object_["@type"] == obj_type:
                    try:
                        # Update the right ID if the object is valid and matches
                        # type of Item
                        object_id = crud.update(object_=object_, id_=id_, type_=object_[
                                                "@type"], session=get_session(), api_name=get_api_name())
                        headers_ = [{"Location": get_hydrus_server_url(
                        ) + get_api_name() + "/" + type_ + "/" + str(object_id)}]
                        response = {
                            "message": "Object with ID %s successfully updated" % (object_id)}
                        return set_response_headers(jsonify(response), headers=headers_)

                    except Exception as e:
                        status_code, message = e.get_HTTP()  # type: ignore
                        return set_response_headers(jsonify(message), status_code=status_code)

            return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

        abort(405)

    def put(self, id_: int, type_: str) -> Response:
        """Add new object_ optional <id_> parameter using HTTP PUT.

        :param id_ - ID of Item to be updated
        :param type_ - Type(Class name) of Item to be updated
        """
        if get_authentication():
            if request.authorization is None:
                return failed_authentication()
            else:
                try:
                    auth = check_authorization(request, get_session())
                    if auth is False:
                        return failed_authentication()
                except Exception as e:
                    status_code, message = e.get_HTTP()  # type: ignore
                    return set_response_headers(jsonify(message), status_code=status_code)

        class_type = get_doc().collections[type_]["collection"].class_.title

        if checkClassOp(class_type, "PUT"):
            # Check if class_type supports PUT operation
            object_ = json.loads(request.data.decode('utf-8'))
            obj_type = getType(class_type, "PUT")
            # Load new object and type
            if validObject(object_):
                if object_["@type"] == obj_type:
                    try:
                        # Add the object with given ID
                        object_id = crud.insert(
                            object_=object_, id_=id_, session=get_session())
                        headers_ = [{"Location": get_hydrus_server_url(
                        ) + get_api_name() + "/" + type_ + "/" + str(object_id)}]
                        response = {
                            "message": "Object with ID %s successfully added" % (object_id)}
                        return set_response_headers(jsonify(response), headers=headers_, status_code=201)
                    except Exception as e:
                        status_code, message = e.get_HTTP()  # type: ignore
                        return set_response_headers(jsonify(message), status_code=status_code)

            return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

        abort(405)

    def delete(self, id_: int, type_: str) -> Response:
        """Delete object with id=id_ from database."""
        if get_authentication():
            if request.authorization is None:
                return failed_authentication()
            else:
                try:
                    auth = check_authorization(request, get_session())
                    if auth is False:
                        return failed_authentication()
                except Exception as e:
                    status_code, message = e.get_HTTP()  # type: ignore
                    return set_response_headers(jsonify(message), status_code=status_code)

        class_type = get_doc().collections[type_]["collection"].class_.title

        if checkClassOp(class_type, "DELETE"):
            # Check if class_type supports PUT operation
            try:
                # Delete the Item with ID == id_
                crud.delete(id_, class_type, session=get_session())
                response = {
                    "message": "Object with ID %s successfully deleted" % (id_)}
                return set_response_headers(jsonify(response))

            except Exception as e:
                status_code, message = e.get_HTTP()  # type: ignore
                return set_response_headers(jsonify(message), status_code=status_code)

        abort(405)


class ItemCollection(Resource):
    """Handle operation related to ItemCollection (a collection of items)."""

    def get(self, type_: str) -> Response:
        """
        Retrieve a collection of items from the database.
        """
        if get_authentication():
            if request.authorization is None:
                return failed_authentication()
            else:
                try:
                    auth = check_authorization(request, get_session())
                    if auth is False:
                        return failed_authentication()
                except Exception as e:
                    status_code, message = e.get_HTTP()  # type: ignore
                    return set_response_headers(jsonify(message), status_code=status_code)

        endpoint_ = checkEndpoint("GET", type_)
        if endpoint_['method']:
            # If endpoint and GET method is supported in the API
            if type_ in get_doc().collections:
                # If collection name in document's collections
                collection = get_doc().collections[type_]["collection"]
                try:
                    # Get collection details from the database
                    response = crud.get_collection(
                        get_api_name(), collection.class_.title, session=get_session())
                    return set_response_headers(jsonify(hydrafy(response)))

                except Exception as e:
                    status_code, message = e.get_HTTP()  # type: ignore
                    return set_response_headers(jsonify(message), status_code=status_code)

            # If class is supported
            elif type_ in get_doc().parsed_classes and type_ + "Collection" not in get_doc().collections:
                try:
                    response = crud.get_single(
                        type_, api_name=get_api_name(), session=get_session())
                    return set_response_headers(jsonify(hydrafy(response)))

                except Exception as e:
                    status_code, message = e.get_HTTP()  # type: ignore
                    return set_response_headers(jsonify(message), status_code=status_code)

        abort(endpoint_['status'])

    def put(self, type_: str) -> Response:
        """
        Method executed for PUT requests.
        Used to add an item to a colllection

        :param type_ - Item type
        """
        if get_authentication():
            # Check if authorization is required
            if request.authorization is None:
                return failed_authentication()
            else:
                try:
                    auth = check_authorization(request, get_session())
                    if auth is False:
                        return failed_authentication()
                except Exception as e:
                    status_code, message = e.get_HTTP()  # type: ignore
                    return set_response_headers(jsonify(message), status_code=status_code)

        endpoint_ = checkEndpoint("PUT", type_)
        if endpoint_['method']:
            # If endpoint and PUT method is supported in the API
            object_ = json.loads(request.data.decode('utf-8'))

            if type_ in get_doc().collections:
                # If collection name in document's collections
                collection = get_doc().collections[type_]["collection"]

                # title of HydraClass object corresponding to collection
                obj_type = collection.class_.title

                if validObject(object_):
                    # If Item in request's JSON is a valid object
                    # ie. @type is one of the keys in object_
                    if object_["@type"] == obj_type:
                        # If the right Item type is being added to the collection
                        try:
                            # Insert object and return location in Header
                            object_id = crud.insert(
                                object_=object_, session=get_session())
                            headers_ = [{"Location": get_hydrus_server_url(
                            ) + get_api_name() + "/" + type_ + "/" + str(object_id)}]
                            response = {
                                "message": "Object with ID %s successfully added" % (object_id)}
                            return set_response_headers(jsonify(response), headers=headers_, status_code=201)
                        except Exception as e:
                            status_code, message = e.get_HTTP()  # type: ignore
                            return set_response_headers(jsonify(message), status_code=status_code)

                return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

            elif type_ in get_doc().parsed_classes and type_ + "Collection" not in get_doc().collections:
                # If type_ is in parsed_classes but is not a collection
                obj_type = getType(type_, "PUT")
                if object_["@type"] == obj_type:
                    if validObject(object_):
                        try:
                            object_id = crud.insert(
                                object_=object_, session=get_session())
                            headers_ = [{"Location": get_hydrus_server_url(
                            ) + get_api_name() + "/" + type_ + "/"}]
                            response = {"message": "Object successfully added"}
                            return set_response_headers(jsonify(response), headers=headers_, status_code=201)
                        except Exception as e:
                            status_code, message = e.get_HTTP()  # type: ignore
                            return set_response_headers(jsonify(message), status_code=status_code)

                return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

        abort(endpoint_['status'])

    def post(self, type_: str) -> Response:
        """
        Method executed for POST requests.
        Used to update a non-collection class.

        :param type_ - Item type
        """
        if get_authentication():
            if request.authorization is None:
                return failed_authentication()
            else:
                try:
                    auth = check_authorization(request, get_session())
                    if auth is False:
                        return failed_authentication()
                except Exception as e:
                    status_code, message = e.get_HTTP()  # type: ignore
                    return set_response_headers(jsonify(message), status_code=status_code)

        endpoint_ = checkEndpoint("POST", type_)
        if endpoint_['method']:
            object_ = json.loads(request.data.decode('utf-8'))
            if type_ in get_doc().parsed_classes and type_ + "Collection" not in get_doc().collections:
                obj_type = getType(type_, "POST")
                if validObject(object_):
                    if object_["@type"] == obj_type:
                        # try:
                        crud.update_single(
                            object_=object_, session=get_session(), api_name=get_api_name())
                        headers_ = [{"Location": get_hydrus_server_url(
                        ) + get_api_name() + "/" + type_ + "/"}]
                        response = {"message": "Object successfully updated"}
                        return set_response_headers(jsonify(response), headers=headers_)
                        # except Exception as e:
                        #     status_code, message = e.get_HTTP()
                        #     return set_response_headers(jsonify(message), status_code=status_code)

                return set_response_headers(jsonify({400: "Data is not valid"}), status_code=400)

        abort(endpoint_['status'])

    def delete(self, type_: str) -> Response:
        """
        Method executed for DELETE requests.
        Used to delete a non-collection class.

        :param type_ - Item type
        """
        if get_authentication():
            if request.authorization is None:
                return failed_authentication()
            else:
                try:
                    auth = check_authorization(request, get_session())
                    if auth is False:
                        return failed_authentication()
                except Exception as e:
                    status_code, message = e.get_HTTP()  # type: ignore
                    return set_response_headers(jsonify(message), status_code=status_code)

        endpoint_ = checkEndpoint("DELETE", type_)
        if endpoint_['method']:
            # No Delete Operation for collections
            if type_ in get_doc().parsed_classes and type_ + "Collection" not in get_doc().collections:
                try:
                    crud.delete_single(type_, session=get_session())
                    response = {"message": "Object successfully deleted"}
                    return set_response_headers(jsonify(response))
                except Exception as e:
                    status_code, message = e.get_HTTP()  # type: ignore
                    return set_response_headers(jsonify(message), status_code=status_code)
        abort(endpoint_['status'])


class Contexts(Resource):
    """Dynamically genereated contexts."""

    def get(self, category: str) -> Response:
        """Return the context for the specified class."""
        if "Collection" in category:

            if category in get_doc().collections:
                # type: Union[Dict[str,Any],Dict[int,str]]
                response = {
                    "@context": get_doc().collections[category]["context"].generate()}
                return set_response_headers(jsonify(response))

            else:
                response = {404: "NOT FOUND"}
                return set_response_headers(jsonify(response), status_code=404)

        else:

            if category in get_doc().parsed_classes:
                response = {
                    "@context": get_doc().parsed_classes[category]["context"].generate()}
                return set_response_headers(jsonify(response))

            else:
                response = {404: "NOT FOUND"}
                return set_response_headers(jsonify(response), status_code=404)


def app_factory(API_NAME: str="api") -> Flask:
    """Create an app object."""
    app = Flask(__name__)

    CORS(app)
    app.url_map.strict_slashes = False
    api = Api(app)

    api.add_resource(Index, "/" + API_NAME + "/", endpoint="api")
    api.add_resource(Vocab, "/" + API_NAME + "/vocab", endpoint="vocab")
    api.add_resource(Contexts, "/" + API_NAME +
                     "/contexts/<string:category>.jsonld", endpoint="contexts")
    api.add_resource(Entrypoint, "/" + API_NAME +
                     "/contexts/EntryPoint.jsonld", endpoint="main_entrypoint")
    api.add_resource(ItemCollection, "/" + API_NAME +
                     "/<string:type_>", endpoint="item_collection")
    api.add_resource(Item, "/" + API_NAME +
                     "/<string:type_>/<int:id_>", endpoint="item")

    return app


if __name__ == "__main__":

    app = app_factory("api")
    app.run(host='127.0.0.1', debug=True, port=8080)
