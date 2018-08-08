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
from hydrus.data.exceptions import (
    ClassNotFound,
    InstanceExists,
    PropertyNotFound,
    NotInstanceProperty,
    NotAbstractProperty,
    InstanceNotFound)
from hydrus.data.user import check_authorization, add_token, check_token, create_nonce
from hydrus.utils import get_session, get_doc, get_api_name, get_hydrus_server_url, get_authentication, get_token

from flask.wrappers import Response
from typing import Dict, List, Any, Union, Optional

def validObject(object_: Dict[str, Any]) -> bool:
    """
        Check if the Dict passed in POST is of valid format or not.
        (if there's an "@type" key in the dict)

        :param object_ - Object to be checked
    """
    if "@type" in object_:
        return True
    return False


def validObjectList(objects_: List[Dict[str, Any]]) -> bool:
    """
        Check if the List of Dicts passed are of the valid format or not.
        (if there's an "@type" key in the dict)

    :param objects_: Object to be checked
    """
    for object_ in objects_:
        if "@type" not in object_:
            return False
    return True


def type_match(object_: List[Dict[str, Any]], obj_type: str) -> bool:
    """
    Checks if the object type matches for every object in list.
    :param object_: List of objects
    :param obj_type: The required object type
    :return: True if all object of list have the right type
            False otherwise
    """
    for obj in object_:
        if obj["@type"] != obj_type:
            return False
    return True


def token_response(token: str) -> Response:
    """
    Return succesful token generation object
    """
    message = {200: "User token generated"}
    response = set_response_headers(jsonify(message), status_code=200,
                                    headers=[{'X-Authorization': token}])
    return response


def failed_authentication(incorrect: bool) -> Response:
    """
    Return failed authentication object.
    """
    if not incorrect:
        message = {401: "Need credentials to authenticate"}
        realm = 'Basic realm="Login required"'
    else:
        message = {401: "Incorrect credentials"}
        realm = 'Basic realm="Incorrect credentials"'
    nonce = create_nonce(get_session())
    response = set_response_headers(jsonify(message), status_code=401, headers=[
                                    {'WWW-Authenticate': realm}, {'X-Authentication': nonce}])
    return response


def set_response_headers(resp: Response,
                         ct: str="application/ld+json",
                         headers: List[Dict[str,
                                            Any]]=[],
                         status_code: int=200) -> Response:
    """Set the response headers."""
    resp.status_code = status_code
    for header in headers:
        resp.headers[list(header.keys())[0]] = header[list(header.keys())[0]]
    resp.headers['Content-type'] = ct
    resp.headers['Link'] = '<' + get_hydrus_server_url() + \
        get_api_name() + '/vocab>; rel="http://www.w3.org/ns/hydra/core#apiDocumentation"'
    return resp


def hydrafy(object_: Dict[str, Any], path: Optional[str]) -> Dict[str, Any]:
    """Add hydra context to objects."""
    if path == object_["@type"]:
        object_["@context"] = "/" + get_api_name() + "/contexts/" + \
            object_["@type"] + ".jsonld"
    else:
        object_["@context"] = "/" + get_api_name() + "/contexts/" + \
            path + ".jsonld"
    return object_


def checkEndpoint(method: str, path: str) -> Dict[str, Union[bool, int]]:
    """Check if endpoint and method is supported in the API."""
    status_val = 404
    if path == 'vocab':
        return {'method': False, 'status': 405}

    for endpoint in get_doc().entrypoint.entrypoint.supportedProperty:
        if path == "/".join(endpoint.id_.split("/")[1:]):
            status_val = 405
            for operation in endpoint.supportedOperation:
                if operation.method == method:
                    status_val = 200
                    return {'method': True, 'status': status_val}
    return {'method': False, 'status': status_val}


def getType(class_path: str, method: str) -> Any:
    """Return the @type of object allowed for POST/PUT."""
    for supportedOp in get_doc(
    ).parsed_classes[class_path]["class"].supportedOperation:
        if supportedOp.method == method:
            return supportedOp.expects.replace("vocab:", "")
    # NOTE: Don't use split, if there are more than one substrings with
    # 'vocab:' not everything will be returned.


def checkClassOp(class_type: str, method: str) -> bool:
    """Check if the Class supports the operation."""
    for supportedOp in get_doc(
    ).parsed_classes[class_type]["class"].supportedOperation:
        if supportedOp.method == method:
            return True
    return False


def verify_user() -> Union[Response, None]:
    """
    Verify the credentials of the user and assign token.
    """
    try:
        auth = check_authorization(request, get_session())
        if auth is False:
            return failed_authentication(True)
        else:
            if get_token():
                token = add_token(request, get_session())
                return token_response(token)
    except Exception as e:
        status_code, message = e.get_HTTP()  # type: ignore
        return set_response_headers(jsonify(message), status_code=status_code)
    return None


def check_authentication_response() -> Union[Response, None]:
    """
    Return the response as per the authentication requirements.
    """
    if get_authentication():
        if get_token():
            token = check_token(request, get_session())
            if not token:
                if request.authorization is None:
                    return failed_authentication(False)
                else:
                    return verify_user()
        elif request.authorization is None:
            return failed_authentication(False)
        else:
            return verify_user()
    return None


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

    def get(self, id_: str, path: str) -> Response:
        """
        GET object with id = id_ from the database.

        :param id : Item ID
        :param path : Path for Item ( Specified in APIDoc @id)
        """
        id_ = str(id_)
        auth_response = check_authentication_response()
        if isinstance(auth_response, Response):
            return auth_response

        class_type = get_doc().collections[path]["collection"].class_.title

        if checkClassOp(class_type, "GET"):
            # Check if class_type supports GET operation
            try:
                # Try getting the Item based on ID and Class type
                response = crud.get(
                    id_,
                    class_type,
                    api_name=get_api_name(),
                    session=get_session())

                return set_response_headers(
                    jsonify(hydrafy(response, path=path)))

            except (ClassNotFound, InstanceNotFound) as e:
                status_code, message = e.get_HTTP()
                return set_response_headers(
                    jsonify(message), status_code=status_code)
        abort(405)

    def post(self, id_: str, path: str) -> Response:
        """Update object of type<path> at ID<id_> with new object_ using HTTP POST.

        :param id_ - ID of Item to be updated
        :param path - Path for Item type( Specified in APIDoc @id)
        """
        id_ = str(id_)
        auth_response = check_authentication_response()
        if isinstance(auth_response, Response):
            return auth_response

        class_type = get_doc().collections[path]["collection"].class_.title

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
                        object_id = crud.update(
                            object_=object_,
                            id_=id_,
                            type_=object_["@type"],
                            session=get_session(),
                            api_name=get_api_name())
                        headers_ = [{"Location": get_hydrus_server_url(
                        ) + get_api_name() + "/" + path + "/" + str(object_id)}]
                        response = {
                            "message": "Object with ID %s successfully updated" %
                            (object_id)}
                        return set_response_headers(
                            jsonify(response), headers=headers_)

                    except (ClassNotFound, InstanceNotFound, InstanceExists, PropertyNotFound) as e:
                        status_code, message = e.get_HTTP()
                        return set_response_headers(
                            jsonify(message), status_code=status_code)

            return set_response_headers(
                jsonify({400: "Data is not valid"}), status_code=400)

        abort(405)

    def put(self, id_: str, path: str) -> Response:
        """Add new object_ optional <id_> parameter using HTTP PUT.

        :param id_ - ID of Item to be updated
        :param path - Path for Item type( Specified in APIDoc @id) to be updated
        """
        id_ = str(id_)
        auth_response = check_authentication_response()
        if isinstance(auth_response, Response):
            return auth_response

        class_type = get_doc().collections[path]["collection"].class_.title
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
                        ) + get_api_name() + "/" + path + "/" + str(object_id)}]
                        response = {
                            "message": "Object with ID %s successfully added" %
                            (object_id)}
                        return set_response_headers(
                            jsonify(response), headers=headers_, status_code=201)
                    except (ClassNotFound, InstanceExists, PropertyNotFound) as e:
                        status_code, message = e.get_HTTP()
                        return set_response_headers(
                            jsonify(message), status_code=status_code)

            return set_response_headers(
                jsonify({400: "Data is not valid"}), status_code=400)

        abort(405)

    def delete(self, id_: str, path: str) -> Response:
        """Delete object with id=id_ from database."""
        id_ = str(id_)
        auth_response = check_authentication_response()
        if isinstance(auth_response, Response):
            return auth_response

        class_type = get_doc().collections[path]["collection"].class_.title

        if checkClassOp(class_type, "DELETE"):
            # Check if class_type supports PUT operation
            try:
                # Delete the Item with ID == id_
                crud.delete(id_, class_type, session=get_session())
                response = {
                    "message": "Object with ID %s successfully deleted" %
                    (id_)}
                return set_response_headers(jsonify(response))

            except (ClassNotFound, InstanceNotFound) as e:
                status_code, message = e.get_HTTP()
                return set_response_headers(
                    jsonify(message), status_code=status_code)

        abort(405)


class ItemCollection(Resource):
    """Handle operation related to ItemCollection (a collection of items)."""

    def get(self, path: str) -> Response:
        """
        Retrieve a collection of items from the database.
        """
        auth_response = check_authentication_response()
        if isinstance(auth_response, Response):
            return auth_response
        endpoint_ = checkEndpoint("GET", path)
        if endpoint_['method']:
            # If endpoint and GET method is supported in the API
            if path in get_doc().collections:
                # If collection name in document's collections
                collection = get_doc().collections[path]["collection"]
                try:
                    # Get collection details from the database
                    response = crud.get_collection(
                        get_api_name(), collection.class_.title, session=get_session(), path=path)
                    return set_response_headers(
                        jsonify(hydrafy(response, path=path)))

                except ClassNotFound as e:
                    status_code, message = e.get_HTTP()
                    return set_response_headers(
                        jsonify(message), status_code=status_code)

            # If class is supported
            elif path in get_doc().parsed_classes and path + "Collection" not in get_doc().collections:
                try:
                    class_type = get_doc().parsed_classes[path]['class'].title
                    response = crud.get_single(
                        class_type,
                        api_name=get_api_name(),
                        session=get_session(),
                        path=path)
                    return set_response_headers(
                        jsonify(hydrafy(response, path=path)))

                except (ClassNotFound, InstanceNotFound) as e:
                    status_code, message = e.get_HTTP()
                    return set_response_headers(
                        jsonify(message), status_code=status_code)

        abort(endpoint_['status'])

    def put(self, path: str) -> Response:
        """
        Method executed for PUT requests.
        Used to add an item to a collection

        :param path - Path for Item type ( Specified in APIDoc @id)
        """
        auth_response = check_authentication_response()
        if isinstance(auth_response, Response):
            return auth_response

        endpoint_ = checkEndpoint("PUT", path)
        if endpoint_['method']:
            # If endpoint and PUT method is supported in the API
            object_ = json.loads(request.data.decode('utf-8'))

            if path in get_doc().collections:
                # If collection name in document's collections
                collection = get_doc().collections[path]["collection"]

                # title of HydraClass object corresponding to collection
                obj_type = collection.class_.title

                if validObject(object_):
                    # If Item in request's JSON is a valid object
                    # ie. @type is one of the keys in object_
                    if object_["@type"] == obj_type:
                        # If the right Item type is being added to the
                        # collection
                        try:
                            # Insert object and return location in Header
                            object_id = crud.insert(
                                object_=object_, session=get_session())
                            headers_ = [{"Location": get_hydrus_server_url(
                            ) + get_api_name() + "/" + path + "/" + str(object_id)}]
                            response = {
                                "message": "Object with ID %s successfully added" %
                                (object_id)}
                            return set_response_headers(
                                jsonify(response), headers=headers_, status_code=201)
                        except (ClassNotFound, InstanceExists, PropertyNotFound) as e:
                            status_code, message = e.get_HTTP()
                            return set_response_headers(
                                jsonify(message), status_code=status_code)

                return set_response_headers(
                    jsonify({400: "Data is not valid"}), status_code=400)

            elif path in get_doc().parsed_classes and path + "Collection" not in get_doc().collections:
                # If path is in parsed_classes but is not a collection
                obj_type = getType(path, "PUT")
                if object_["@type"] == obj_type:
                    if validObject(object_):
                        try:
                            object_id = crud.insert(
                                object_=object_, session=get_session())
                            headers_ = [{"Location": get_hydrus_server_url(
                            ) + get_api_name() + "/" + path + "/"}]
                            response = {"message": "Object successfully added"}
                            return set_response_headers(
                                jsonify(response), headers=headers_, status_code=201)
                        except (ClassNotFound, InstanceExists, PropertyNotFound) as e:
                            status_code, message = e.get_HTTP()
                            return set_response_headers(
                                jsonify(message), status_code=status_code)

                return set_response_headers(
                    jsonify({400: "Data is not valid"}), status_code=400)

        abort(endpoint_['status'])

    def post(self, path: str) -> Response:
        """
        Method executed for POST requests.
        Used to update a non-collection class.

        :param path - Path for Item type ( Specified in APIDoc @id)
        """
        auth_response = check_authentication_response()
        if isinstance(auth_response, Response):
            return auth_response

        endpoint_ = checkEndpoint("POST", path)
        if endpoint_['method']:
            object_ = json.loads(request.data.decode('utf-8'))
            if path in get_doc().parsed_classes and path + \
                    "Collection" not in get_doc().collections:
                obj_type = getType(path, "POST")
                if validObject(object_):
                    if object_["@type"] == obj_type:
                        try:
                            crud.update_single(
                                object_=object_,
                                session=get_session(),
                                api_name=get_api_name(),
                                path=path)
                            headers_ = [{"Location": get_hydrus_server_url(
                            ) + get_api_name() + "/" + path + "/"}]
                            response = {
                                "message": "Object successfully updated"}
                            return set_response_headers(
                                jsonify(response), headers=headers_)
                        except (ClassNotFound, InstanceNotFound, InstanceExists, PropertyNotFound) as e:
                            status_code, message = e.get_HTTP()
                            return set_response_headers(
                                jsonify(message), status_code=status_code)

                return set_response_headers(
                    jsonify({400: "Data is not valid"}), status_code=400)

        abort(endpoint_['status'])

    def delete(self, path: str) -> Response:
        """
        Method executed for DELETE requests.
        Used to delete a non-collection class.

        :param path - Path for Item ( Specified in APIDoc @id)
        """
        auth_response = check_authentication_response()
        if isinstance(auth_response, Response):
            return auth_response

        endpoint_ = checkEndpoint("DELETE", path)
        if endpoint_['method']:
            # No Delete Operation for collections
            if path in get_doc().parsed_classes and path + \
                    "Collection" not in get_doc().collections:
                try:
                    class_type = get_doc().parsed_classes[path]['class'].title
                    crud.delete_single(class_type, session=get_session())
                    response = {"message": "Object successfully deleted"}
                    return set_response_headers(jsonify(response))
                except (ClassNotFound, InstanceNotFound) as e:
                    status_code, message = e.get_HTTP()
                    return set_response_headers(
                        jsonify(message), status_code=status_code)
        abort(endpoint_['status'])


class Items(Resource):

    def put(self, path, int_list="") -> Response:
        """
        To insert multiple objects into the database
        :param path: endpoint
        :param int_list: Optional String containing ',' separated ID's
        :return:
        """
        auth_response = check_authentication_response()
        if isinstance(auth_response, Response):
            return auth_response

        endpoint_ = checkEndpoint("PUT", path)
        if endpoint_['method']:
            # If endpoint and PUT method is supported in the API
            object_ = json.loads(request.data.decode('utf-8'))
            object_ = object_["data"]
            if path in get_doc().collections:
                # If collection name in document's collections
                collection = get_doc().collections[path]["collection"]
                # title of HydraClass object corresponding to collection
                obj_type = collection.class_.title
                if validObjectList(object_):
                    type_result = type_match(object_, obj_type)
                    # If Item in request's JSON is a valid object
                    # ie. @type is one of the keys in object_
                    if type_result:
                        # If the right Item type is being added to the
                        # collection
                        try:
                            # Insert object and return location in Header
                            object_id = crud.insert_multiple(
                                objects_=object_, session=get_session(), id_=int_list)
                            headers_ = [{"Location": get_hydrus_server_url(
                            ) + get_api_name() + "/" + path + "/" + str(object_id)}]
                            response = {
                                "message": "Object with ID %s successfully added" %
                                (object_id)}
                            return set_response_headers(
                                jsonify(response), headers=headers_, status_code=201)
                        except (ClassNotFound, InstanceExists, PropertyNotFound) as e:
                            status_code, message = e.get_HTTP()
                            return set_response_headers(
                                jsonify(message), status_code=status_code)

                return set_response_headers(
                    jsonify({400: "Data is not valid"}), status_code=400)

            
        abort(endpoint_['status'])

    def delete(self, path, int_list):
        """
        To delete multiple objects
        :param path: endpoints
        :param int_list: Optional String containing ',' separated ID's
        :return:
        """
        auth_response = check_authentication_response()
        if isinstance(auth_response, Response):
            return auth_response
        class_type = get_doc().collections[path]["collection"].class_.title

        if checkClassOp(class_type, "DELETE"):
            # Check if class_type supports PUT operation
            try:
                # Delete the Item with ID == id_
                crud.delete_multiple(
                    int_list, class_type, session=get_session())
                response = {
                    "message": "Object with ID %s successfully deleted" %
                    (int_list.split(','))}
                return set_response_headers(jsonify(response))

            except (ClassNotFound, InstanceNotFound) as e:
                status_code, message = e.get_HTTP()
                return set_response_headers(
                    jsonify(message), status_code=status_code)

        abort(405)


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
    app.config['SECRET_KEY'] = 'secret key'
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
                     "/<string:path>", endpoint="item_collection")
    api.add_resource(Item, "/" + API_NAME +
                     "/<string:path>/<uuid:id_>", endpoint="item")
    api.add_resource(Items, "/" + API_NAME +
                     "/<string:path>/add/<int_list>", "/" + API_NAME +
                     "/<string:path>/add", "/" + API_NAME +
                     "/<string:path>/delete/<int_list>")

    return app


if __name__ == "__main__":

    app = app_factory("api")
    app.run(host='127.0.0.1', debug=True, port=8080)
