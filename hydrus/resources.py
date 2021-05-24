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
    hydrus.auth.authenticate : Decorator for checking authentication of each request
    hydrus.utils.get_session : Gets the database session for the server
    hydrus.utils.get_doc : Function which gets the server API documentation
    hydrus.utils.get_api_name : Function which gets the server API name
    hydrus.utils.get_hydrus_server_url : Function the gets the server URL
    hydrus.utils.get_authentication : Function that checks whether API needs to be
    authenticated or not
    hydrus.utils.get_collections_and_parsed_classes: Function that returns
    all the collections and parsed classes in the API documentation
"""  # nopep8

import json

from flask import Response, jsonify, request, abort
from flask_restful import Resource

from hydrus.auth import authenticate
from hydrus.helpers import (
    set_response_headers,
    checkClassOp,
    checkEndpoint,
    check_writeable_props,
    get_context,
    get_fragments
)
from hydrus.utils import get_doc, get_collections_and_parsed_classes
from hydrus.itemhelpers import (
    items_get_check_support,
    items_post_check_support,
    items_put_check_support,
    items_delete_check_support,
    member_get_check_support,
    member_delete_check_support
)
from hydrus.item_collection_helpers import (
    item_collection_get_response,
    item_collection_put_response
)
from hydrus.items_helpers import (
    items_put_response,
    items_delete_response
)


class Index(Resource):
    """Class for the EntryPoint."""

    def get(self) -> Response:
        """Return main entrypoint for the api."""
        return set_response_headers(jsonify(get_doc().entrypoint.get()))


class Vocab(Resource):
    """Vocabulary for Hydra."""

    def get(self) -> Response:
        """Return the main hydra vocab or a fragment of the main hydra vocab."""
        try:
            resource = request.args.getlist('resource')[0]
            return set_response_headers(jsonify(get_fragments(resource)))
        except:
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
    @authenticate
    def get(self, id_: str, path: str) -> Response:
        """
        GET object with id = id_ from the database.
        :param id_ : Item ID
        :param path : Path for Item ( Specified in APIDoc @id)
        :return : object with id=id_
        """
        id_ = str(id_)
        collections, parsed_classes = get_collections_and_parsed_classes()
        is_collection = False
        if path in parsed_classes:
            class_path = path
            class_type = parsed_classes[path]['class'].title
        if path in collections:
            item_class = collections[path]["collection"]
            class_type = item_class.name
            # Get path of the collection-class
            class_path = item_class.path
            is_collection = True
        if checkClassOp(class_path, "GET"):
            return items_get_check_support(id_, class_type, class_path, path, is_collection)
        abort(405)

    @authenticate
    def post(self, id_: str, path: str) -> Response:
        """
        Update object of type<path> at ID<id_> with new object_ using HTTP POST.
        :param id_ - ID of Item to be updated
        :param path - Path for Item type( Specified in APIDoc @id)
        """
        id_ = str(id_)
        collections, parsed_classes = get_collections_and_parsed_classes()
        is_collection = False
        if path in parsed_classes:
            class_path = path
        if path in collections:
            item_class = collections[path]["collection"]
            class_path = item_class.path
            is_collection = True
        object_ = json.loads(request.data.decode('utf-8'))
        if checkClassOp(class_path, "POST") and check_writeable_props(class_path, object_):
            return items_post_check_support(id_, object_, class_path, path, is_collection)
        abort(405)

    @authenticate
    def put(self, id_: str, path: str) -> Response:
        """
        Add new object_ optional <id_> parameter using HTTP PUT.
        :param id_ - ID of Item to be updated
        :param path - Path for Item type( Specified in APIDoc @id) to be updated
        """
        id_ = str(id_)
        collections, parsed_classes = get_collections_and_parsed_classes()
        is_collection = False
        if path in parsed_classes:
            class_path = path
        if path in collections:
            item_class = collections[path]["collection"]
            class_path = item_class.path
            is_collection = True
        if checkClassOp(class_path, "PUT"):
            return items_put_check_support(id_, class_path, path, is_collection)
        abort(405)

    @authenticate
    def delete(self, id_: str, path: str) -> Response:
        """
        Delete object with id=id_ from database.
        :param id_ - ID of Item to be deleted
        :param path - Path for Item type( Specified in APIDoc @id) to be deleted
        """
        id_ = str(id_)
        collections, parsed_classes = get_collections_and_parsed_classes()
        is_collection = False
        if path in parsed_classes:
            class_path = path
            class_type = parsed_classes[path]['class'].title
        if path in collections:
            item_class = collections[path]["collection"]
            class_type = item_class.name
            # Get path of the collection-class
            class_path = item_class.path
            is_collection = True
        if checkClassOp(class_path, "DELETE"):
            return items_delete_check_support(id_, class_type, path, is_collection)
        abort(405)


class ItemCollection(Resource):
    """Handle operation related to ItemCollection (a collection of items)."""
    @authenticate
    def get(self, path: str) -> Response:
        """
        Retrieve a collection of items from the database.
        :param path : Path of the Collection
        :return : collection of items
        """
        endpoint_ = checkEndpoint("GET", path)
        if not endpoint_['method']:
            # If endpoint and Get method not supported in the API
            abort(endpoint_['status'])
        return item_collection_get_response(path)

    @authenticate
    def put(self, path: str) -> Response:
        """
        Method executed for PUT requests.
        Used to add an item to a collection
        :param path - Path for Item type ( Specified in APIDoc @id)
        """
        endpoint_ = checkEndpoint("PUT", path)
        if not endpoint_['method']:
            # If endpoint and PUT method is not supported in the API
            abort(endpoint_['status'])
        return item_collection_put_response(path)


class ItemMember(Resource):
    """Handles operations(GET,DELETE) related to member of an Item(Collection).
    (Item should be hydra:Collection)"""
    @authenticate
    def get(self, id_: str, path: str, collection_id_: str) -> Response:
        """
        GET object with collection_id = collection_id_
        and member = id_ (member of a collection) from the database.
        :param id_ : Item ID (Member)
        :param collection_id_ : Item ID (Collection)
        :param path : Path for Item ( Specified in APIDoc @id)
        :return : object with member=id_ and collection_id=collection_id_
        """
        collection_id = str(collection_id_)
        member_id = str(id_)
        collections, parsed_classes = get_collections_and_parsed_classes()
        if path in parsed_classes:
            abort(405)
        if path in collections:
            item_class = collections[path]["collection"]
            class_type = item_class.name
            # Get path of the collection-class
            class_path = item_class.path
        if checkClassOp(class_path, "GET"):
            return member_get_check_support(collection_id, member_id, class_type, class_path, path)
        abort(405)

    @authenticate
    def delete(self, id_: str, path: str, collection_id_: str) -> Response:
        """
        Delete object with id=id_ from database.
        :param id_ - ID of Item to be deleted
        :param path - Path for Item type( Specified in APIDoc @id) to be deleted
        """
        collection_id = str(collection_id_)
        member_id = str(id_)
        collections, parsed_classes = get_collections_and_parsed_classes()
        if path in parsed_classes:
            abort(405)
        if path in collections:
            item_class = collections[path]["collection"]
            class_type = item_class.name
            # Get path of the collection-class
            class_path = item_class.path
        if checkClassOp(class_path, "DELETE"):
            return member_delete_check_support(collection_id, member_id, class_type, path)
        abort(405)


class Items(Resource):
    """Handles operations(PUT,DELETE) related to multiple objects.
    (Item should be hydra:Class)"""
    @authenticate
    def put(self, path, int_list="") -> Response:
        """
        To insert multiple objects into the database
        :param path: endpoint
        :param int_list: Optional String containing ',' separated ID's
        :return:
        """
        endpoint_ = checkEndpoint("PUT", path)
        if not endpoint_['method']:
            # If endpoint and PUT method is not supported in the API
            abort(endpoint_['status'])
        return items_put_response(path, int_list)

    @authenticate
    def delete(self, path, int_list):
        """
        To delete multiple objects
        :param path: endpoints
        :param int_list: Optional String containing ',' separated ID's
        :return:
        """
        return items_delete_response(path, int_list)


class Contexts(Resource):
    """Dynamically generated contexts."""

    def get(self, category: str) -> Response:
        """Return the context for the specified class."""
        return get_context(category)
