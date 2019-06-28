"""Imports :

    flask.json.jsonify : Turns the JSON output into a Response object with the
    application/json mimetype Ref- http://flask.pocoo.org/docs/0.12/api

    flask.request : The request object used by default in Flask.
    Remembers the matched endpoint and view arguments.
    Ref - http://flask.pocoo.org/docs/0.12/api

    flask.abort : Raises an HTTPException for the given status code or WSGI
    application: Ref - http://flask.pocoo.org/docs/0.12/api

    flask_restful.Resource : Represents an abstract RESTful resource.
    Ref - http://flask-restful.readthedocs.io/en/latest/api.html


    hydrus.data.crud : Function/Class to perform basic CRUD operations for the server
    hydrus.data.user.check_authorization : Funcion checks if the request object has the
    correct authorization
    hydrus.utils.get_session : Gets the database session for the server
    hydrus.utils.get_doc : Function which gets the server API documentation
    hydrus.utils.get_api_name : Function which gets the server API name
    hydrus.utils.get_hydrus_server_url : Function the gets the server URL
    hydrus.utils.get_authentication : Function that checks whether API needs to be
    authenticated or not

"""  # nopep8

import json
from typing import Dict, Any, Union
from flask import Response, jsonify, request, abort
from flask_restful import Resource
from hydra_python_core.doc_writer import HydraStatus, HydraError

from hydrus.auth import check_authentication_response
from hydrus.data import crud
from hydrus.data.exceptions import (
    ClassNotFound,
    InstanceExists,
    PropertyNotFound,
    InstanceNotFound,
    PageNotFound,
    InvalidSearchParameter)
from hydrus.helpers import (
    set_response_headers,
    checkClassOp,
    getType,
    validObject,
    checkEndpoint,
    validObjectList,
    type_match,
    hydrafy,
    check_read_only_props,
    check_required_props,
    add_iri_template,
    finalize_response)
from hydrus.utils import (get_session,
    get_doc,
    get_api_name,
    get_hydrus_server_url,
    get_page_size,
    get_pagination)


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
    """Handles all operations(GET, POST, PATCH, DELETE) on Items
    (item can be anything depending upon the vocabulary)."""

    def get(self, id_: str, path: str) -> Response:
        """
        GET object with id = id_ from the database.

        :param id_ : Item ID
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

                response = finalize_response(class_type, response)
                return set_response_headers(
                    jsonify(hydrafy(response, path=path)))

            except (ClassNotFound, InstanceNotFound) as e:
                error = e.get_HTTP()
                return set_response_headers(jsonify(error.generate()), status_code=error.code)
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
        object_ = json.loads(request.data.decode('utf-8'))
        if checkClassOp(class_type, "POST") and check_read_only_props(class_type, object_):
            # Check if class_type supports POST operation
            obj_type = getType(class_type, "POST")
            # Load new object and type
            if validObject(object_) and object_["@type"] == obj_type and check_required_props(
                    class_type, object_):
                try:
                    # Update the right ID if the object is valid and matches
                    # type of Item
                    object_id = crud.update(
                        object_=object_,
                        id_=id_,
                        type_=object_["@type"],
                        session=get_session(),
                        api_name=get_api_name())
                    headers_ = [{"Location": "{}{}/{}/{}".format(
                            get_hydrus_server_url(), get_api_name(), path, object_id)}]
                    status_description = "Object with ID {} successfully updated".format(object_id)
                    status = HydraStatus(code=200, title="Object updated", desc=status_description)
                    return set_response_headers(jsonify(status.generate()), headers=headers_)

                except (ClassNotFound, InstanceNotFound, InstanceExists, PropertyNotFound) as e:
                    error = e.get_HTTP()
                    return set_response_headers(jsonify(error.generate()), status_code=error.code)
            else:
                error = HydraError(code=400, title="Data is not valid")
                return set_response_headers(jsonify(error.generate()), status_code=error.code)
        else:
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
            if validObject(object_) and object_["@type"] == obj_type and check_required_props(
                    class_type, object_):
                try:
                    # Add the object with given ID
                    object_id = crud.insert(object_=object_, id_=id_, session=get_session())
                    headers_ = [{"Location": "{}{}/{}/{}".format(
                            get_hydrus_server_url(), get_api_name(), path, object_id)}]
                    status_description = "Object with ID {} successfully added".format(object_id)
                    status = HydraStatus(code=201, title="Object successfully added.",
                                         desc=status_description)
                    return set_response_headers(
                        jsonify(status.generate()), headers=headers_, status_code=status.code)
                except (ClassNotFound, InstanceExists, PropertyNotFound) as e:
                    error = e.get_HTTP()
                    return set_response_headers(jsonify(error.generate()), status_code=error.code)
            else:
                error = HydraError(code=400, title="Data is not valid")
                return set_response_headers(jsonify(error.generate()), status_code=error.code)
        else:
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
                status_description = "Object with ID {} successfully deleted".format(id_)
                status = HydraStatus(code=200, title="Object successfully created.",
                                     desc=status_description)
                return set_response_headers(jsonify(status.generate()))

            except (ClassNotFound, InstanceNotFound) as e:
                error = e.get_HTTP()
                return set_response_headers(jsonify(error.generate()), status_code=error.code)

        abort(405)


class ItemCollection(Resource):
    """Handle operation related to ItemCollection (a collection of items)."""

    def get(self, path: str) -> Response:
        """
        Retrieve a collection of items from the database.
        """
        search_params = request.args.to_dict()
        auth_response = check_authentication_response()
        if isinstance(auth_response, Response):
            return auth_response
        endpoint_ = checkEndpoint("GET", path)
        if not endpoint_['method']:
            # If endpoint and Get method not supported in the API
            abort(endpoint_['status'])
        elif path in get_doc().collections:
            # If endpoint and GET method is supported in the API
            # and collection name in document's collections
            collection = get_doc().collections[path]["collection"]
            try:
                # Get collection details from the database
                if get_pagination():
                    # Get paginated response
                    response = crud.get_collection(
                        get_api_name(), collection.class_.title, session=get_session(),
                        paginate=True, path=path, page_size=get_page_size(), search_params=search_params)
                else:
                    # Get whole collection
                    response = crud.get_collection(
                        get_api_name(), collection.class_.title, session=get_session(),
                        paginate=False, path=path, search_params=search_params)

                response["search"] = add_iri_template(class_type=collection.class_.title,
                                                      API_NAME=get_api_name(), path=path)

                return set_response_headers(jsonify(hydrafy(response, path=path)))

            except (ClassNotFound, PageNotFound, InvalidSearchParameter) as e:
                error = e.get_HTTP()
                return set_response_headers(jsonify(error.generate()), status_code=error.code)

        # If endpoint and GET method is supported in the API and class is supported
        elif path in get_doc().parsed_classes and "{}Collection".format(
                path) not in get_doc().collections:
            try:
                class_type = get_doc().parsed_classes[path]['class'].title
                response = crud.get_single(
                    class_type,
                    api_name=get_api_name(),
                    session=get_session(),
                    path=path)
                response = finalize_response(class_type, response)
                return set_response_headers(jsonify(hydrafy(response, path=path)))

            except (ClassNotFound, InstanceNotFound) as e:
                error = e.get_HTTP()
                return set_response_headers(jsonify(error.generate()), status_code=error.code)

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

                if validObject(object_) and object_["@type"] == obj_type and check_required_props(
                        obj_type, object_):
                    # If Item in request's JSON is a valid object ie. @type is a key in object_
                    # and the right Item type is being added to the collection
                    try:
                        # Insert object and return location in Header
                        object_id = crud.insert(object_=object_, session=get_session())
                        headers_ = [
                            {"Location": "{}{}/{}/{}".format(
                                get_hydrus_server_url(), get_api_name(), path, object_id)}]
                        status_description = "Object with ID {} successfully added".format(object_id)
                        status = HydraStatus(code=201, title="Object successfully added",
                                             desc=status_description)
                        return set_response_headers(
                            jsonify(status.generate()), headers=headers_, status_code=status.code)
                    except (ClassNotFound, InstanceExists, PropertyNotFound) as e:
                        error = e.get_HTTP()
                        return set_response_headers(jsonify(error.generate()), status_code=error.code)

                else:
                    error = HydraError(code=400, title="Data is not valid")
                    return set_response_headers(jsonify(error.generate()), status_code=error.code)

            elif path in get_doc().parsed_classes and "{}Collection".format(path) not in get_doc(
            ).collections:
                # If path is in parsed_classes but is not a collection
                obj_type = getType(path, "PUT")
                if object_["@type"] == obj_type and validObject(object_) and check_required_props(
                        obj_type, object_):
                    try:
                        object_id = crud.insert(object_=object_, session=get_session())
                        headers_ = [{"Location": "{}{}/{}/".format(
                                get_hydrus_server_url(), get_api_name(), path)}]
                        status = HydraStatus(code=201, title="Object successfully added")
                        return set_response_headers(
                            jsonify(status.generate()), headers=headers_, status_code=status.code)
                    except (ClassNotFound, InstanceExists, PropertyNotFound) as e:
                        error = e.get_HTTP()
                        return set_response_headers(jsonify(error.generate()), status_code=error.code)

                else:
                    error = HydraError(code=400, title="Data is not valid")
                    return set_response_headers(jsonify(error.generate()), status_code=error.code)

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
            if path in get_doc().parsed_classes and "{}Collection".format(path) not in get_doc(
            ).collections:
                obj_type = getType(path, "POST")
                if check_read_only_props(obj_type, object_):
                    if object_["@type"] == obj_type and check_required_props(
                            obj_type, object_) and validObject(object_):
                        try:
                            crud.update_single(
                                object_=object_,
                                session=get_session(),
                                api_name=get_api_name(),
                                path=path)

                            headers_ = [
                                {"Location": "{}/{}/".format(
                                    get_hydrus_server_url(), get_api_name(), path)}]
                            status = HydraStatus(code=200, title="Object successfully added")
                            return set_response_headers(
                                jsonify(status.generate()), headers=headers_)
                        except (ClassNotFound, InstanceNotFound,
                                InstanceExists, PropertyNotFound) as e:
                            error = e.get_HTTP()
                            return set_response_headers(
                                jsonify(error.generate()), status_code=error.code)

                    error = HydraError(code=400, title="Data is not valid")
                    return set_response_headers(jsonify(error.generate()), status_code=error.code)
                else:
                    abort(405)

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
        if not endpoint_['method']:
            abort(endpoint_['status'])
        elif path in get_doc().parsed_classes and "{}Collection".format(
                path) not in get_doc().collections:
            # No Delete Operation for collections
            try:
                class_type = get_doc().parsed_classes[path]['class'].title
                crud.delete_single(class_type, session=get_session())
                status = HydraStatus(code=200, title="Object successfully added")
                return set_response_headers(jsonify(status.generate()))
            except (ClassNotFound, InstanceNotFound) as e:
                error = e.get_HTTP()
                return set_response_headers(
                    jsonify(error.generate()), status_code=error.code)


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
                incomplete_objects = list()
                for obj in object_:
                    if not check_required_props(obj_type, obj):
                        incomplete_objects.append(obj)
                        object_.remove(obj)
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
                            headers_ = [{"Location": "{}{}/{}/{}".format(
                                    get_hydrus_server_url(), get_api_name(), path, object_id)}]
                            if len(incomplete_objects) > 0:
                                status = HydraStatus(code=202, title="Object(s) missing required property")
                                response = status.generate()
                                response["objects"] = incomplete_objects
                                return set_response_headers(
                                    jsonify(response), headers=headers_, status_code=status.code)
                            else:
                                status_description = "Objects with ID {} successfully added".format(object_id)
                                status = HydraStatus(code=201, title="Objects successfully added",
                                                     desc=status_description)
                                return set_response_headers(
                                    jsonify(status.generate()), headers=headers_, status_code=status.code)
                        except (ClassNotFound, InstanceExists, PropertyNotFound) as e:
                            error = e.get_HTTP()
                            return set_response_headers(jsonify(error.generate()), status_code=error.code)

                error = HydraError(code=400, title="Data is not valid")
                return set_response_headers(jsonify(error.generate()), status_code=error.code)

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
                crud.delete_multiple(int_list, class_type, session=get_session())
                status_description = "Objects with ID {} successfully deleted".format(int_list.split(','))
                status = HydraStatus(code=200, title="Objects successfully deleted", desc=status_description)
                return set_response_headers(jsonify(status.generate()))

            except (ClassNotFound, InstanceNotFound) as e:
                error = e.get_HTTP()
                return set_response_headers(jsonify(error.generate()), status_code=error.code)

        abort(405)


class Contexts(Resource):
    """Dynamically genereated contexts."""

    def get(self, category: str) -> Response:
        """Return the context for the specified class."""
        # Check for collection
        if category in get_doc().collections:
            # type: Union[Dict[str,Any],Dict[int,str]]
            response = {"@context": get_doc().collections[category]["context"].generate()}
            return set_response_headers(jsonify(response))
        # Check for non collection class
        elif category in get_doc().parsed_classes:
            response = {"@context": get_doc().parsed_classes[category]["context"].generate()}
            return set_response_headers(jsonify(response))
        else:
            error = HydraError(code=404, title="NOT FOUND", desc="Context not found")
            return set_response_headers(jsonify(error.generate()), status_code=error.code)
