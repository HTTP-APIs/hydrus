"""Helper functions for Item Collection"""

import json
from functools import partial

from flask import Response, jsonify, request, abort
from hydra_python_core.doc_writer import HydraStatus, HydraError, DocUrl

from hydrus.data import crud
from hydrus.data.exceptions import (
    ClassNotFound,
    InstanceExists,
    PropertyNotFound,
    PageNotFound,
    InvalidSearchParameter,
    OffsetOutOfRange,
    PropertyNotGiven,
    InvalidDateTimeFormat
)

from hydrus.data.helpers import (
    set_response_headers,
    getType,
    hydrafy,
    add_iri_template,
    error_response,
    validate_object,
    parse_collection_members,
    get_collections_and_parsed_classes,
)

from hydrus.utils import (
    get_session,
    get_api_name,
    get_hydrus_server_url,
    get_page_size,
    get_pagination,
    get_doc
)


def item_collection_get_response(path: str) -> Response:
    """
    Handles GET operation on item collection classes.

    :param path: Path for Item Collection
    :type path: str
    :return: Appropriate response for the GET operation.
    :rtype: Response
    """
    search_params = request.args.to_dict()
    collections, parsed_classes = get_collections_and_parsed_classes()
    api_name = get_api_name()
    expanded_base_url = DocUrl.doc_url
    # If endpoint and GET method is supported in the API and class is supported
    if path in parsed_classes:
        abort(405)
    if path in collections:
        collection = collections[path]["collection"]
        class_name = collection.manages["object"].split(expanded_base_url)[1]
        collection_manages_class = parsed_classes[class_name]["class"]
        class_type = collection_manages_class.title
        class_path = collection_manages_class.path
    try:
        # Get collection details from the database
        # create partial function for crud operation
        crud_response = partial(
            crud.get_collection,
            api_name,
            class_type,
            session=get_session(),
            path=path,
            search_params=search_params,
            collection=False,
        )
        if get_pagination():
            # Get paginated response
            response = crud_response(paginate=True, page_size=get_page_size())
        else:
            # Get whole collection
            response = crud_response(paginate=False)

        response["search"] = add_iri_template(
            path=class_path, API_NAME=api_name, collection_path=path
        )

        return set_response_headers(jsonify(hydrafy(response, path=path)))

    except (ClassNotFound, PageNotFound, InvalidSearchParameter, OffsetOutOfRange) as e:
        error = e.get_HTTP()
        return error_response(error)


def item_collection_put_response(path: str) -> Response:
    """
    Handles PUT operation on item collection classes.

    :param path: Path for Item Collection
    :type path: str
    :return: Appropriate response for the PUT operation.
    :rtype: Response
    """
    object_ = json.loads(request.data.decode("utf-8"))
    doc_object = get_doc()
    collections, parsed_classes = get_collections_and_parsed_classes()
    is_collection = False
    if path in parsed_classes:
        class_path = path
        is_collection = False
        obj_type = getType(path, "PUT")
    elif path in collections:
        collection = collections[path]["collection"]
        class_path = collection.path
        obj_type = collection.name
        is_collection = True
    if validate_object(object_, obj_type, class_path):
        # If Item in request's JSON is a valid object ie. @type is a key in object_
        # and the right Item type is being added to the collection
        if is_collection:
            object_ = parse_collection_members(object_)
        try:
            # Insert object and return location in Header
            object_id = crud.insert(
                object_=object_, session=get_session(), doc_=doc_object, collection=is_collection
            )
            resource_url = (
                f"{get_hydrus_server_url()}{get_api_name()}/{path}/{object_id}"
            )
            headers_ = [{"Location": resource_url}]
            status_description = f"Object with ID {object_id} successfully added"
            status = HydraStatus(
                code=201, title="Object successfully added", desc=status_description
            )
            status_response = status.generate()
            status_response["iri"] = resource_url
            return set_response_headers(
                jsonify(status_response), headers=headers_, status_code=status.code
            )
        except (ClassNotFound, InstanceExists, PropertyNotFound,
                PropertyNotGiven, InvalidDateTimeFormat) as e:
            error = e.get_HTTP()
            return error_response(error)
    else:
        error = HydraError(code=400, title="Data is not valid")
        return error_response(error)
