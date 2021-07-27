"""Helper functions for Item Collection"""
import json
from flask import Response, jsonify, request, abort
from hydra_python_core.doc_writer import HydraStatus, HydraError
from hydrus.data import crud
from hydrus.data.exceptions import (
    ClassNotFound,
    InstanceExists,
    PropertyNotFound,
    InstanceNotFound,
    InvalidDateTimeFormat
)
from hydrus.data.helpers import (
    checkClassOp,
    validObjectList,
    type_match,
    check_required_props,
    send_sync_update,
    get_link_props_for_multiple_objects,
    get_iri_from_int_list,
    error_response,
    getType,
    get_collections_and_parsed_classes,
)
from hydrus.utils import (
    get_session,
    get_api_name,
    get_hydrus_server_url,
    set_response_headers,
    get_doc
)
from hydrus.extensions.socketio_factory import socketio


def items_put_response(path: str, int_list="") -> Response:
    """
    Handles PUT operation to insert multiple items.

    :param path: Path for Item Collection
    :type path: str
    :param int_list: Optional String containing ',' separated ID's
    :type int_list: List
    :return: Appropriate response for the PUT operation on multiple items.
    :rtype: Response
    """
    object_ = json.loads(request.data.decode("utf-8"))
    doc = get_doc()
    object_ = object_["data"]
    _, parsed_classes = get_collections_and_parsed_classes()
    if path in parsed_classes:
        class_path = path
        obj_type = getType(path, "PUT")
        incomplete_objects = []
        for obj in object_:
            if not check_required_props(class_path, obj):
                incomplete_objects.append(obj)
                object_.remove(obj)
        link_props_list, link_type_check = get_link_props_for_multiple_objects(
            class_path, object_
        )
        if validObjectList(object_) and link_type_check:
            type_result = type_match(object_, obj_type)
            # If Item in request's JSON is a valid object
            # ie. @type is one of the keys in object_
            if type_result:
                # If the right Item type is being added to the
                # collection
                try:
                    # Insert object and return location in Header
                    object_id = crud.insert_multiple(
                        doc, objects_=object_, session=get_session(), id_=int_list
                    )
                    headers_ = [
                        {
                            "Location": f"{get_hydrus_server_url()}"
                            f"{get_api_name()}/{path}/{object_id}"
                        }
                    ]
                    if len(incomplete_objects) > 0:
                        status = HydraStatus(
                            code=202, title="Object(s) missing required property"
                        )
                        response = status.generate()
                        response["objects"] = incomplete_objects
                        return set_response_headers(
                            jsonify(response), headers=headers_, status_code=status.code
                        )
                    else:
                        path_url = f"{get_hydrus_server_url()}{get_api_name()}/{path}"
                        response_url_list = get_iri_from_int_list(path_url, object_id)
                        status_description = (
                            f"Objects with ID {object_id} successfully added"
                        )
                        status = HydraStatus(
                            code=201,
                            title="Objects successfully added",
                            desc=status_description,
                        )
                        status_response = status.generate()
                        status_response["iri"] = response_url_list
                        return set_response_headers(
                            jsonify(status_response),
                            headers=headers_,
                            status_code=status.code,
                        )
                except (ClassNotFound, InstanceExists,
                        PropertyNotFound, InvalidDateTimeFormat) as e:
                    error = e.get_HTTP()
                    return error_response(error)

        error = HydraError(code=400, title="Data is not valid")
        return error_response(error)


def items_delete_response(path: str, int_list="") -> Response:
    """
    Handles DELETE operation to insert multiple items.

    :param path: Path for Item Collection
    :type path: str
    :param int_list: Optional String containing ',' separated ID's
    :type int_list: List
    :return: Appropriate response for the DELETE operation on multiple items.
    :rtype: Response
    """
    _, parsed_classes = get_collections_and_parsed_classes()
    if path in parsed_classes:
        class_type = parsed_classes[path]["class"].title

    if checkClassOp(class_type, "DELETE"):
        # Check if class_type supports PUT operation
        try:
            # Delete the Item with ID == id_
            crud.delete_multiple(int_list, class_type, session=get_session())
            method = "DELETE"
            path_url = f"{get_hydrus_server_url()}{get_api_name()}/{path}"
            last_job_id = crud.get_last_modification_job_id(session=get_session())
            id_list = int_list.split(",")
            for item in id_list:
                resource_url = path_url + item
                new_job_id = crud.insert_modification_record(
                    method, resource_url, session=get_session()
                )
                send_sync_update(
                    socketio=socketio,
                    new_job_id=new_job_id,
                    last_job_id=last_job_id,
                    method=method,
                    resource_url=resource_url,
                )
                last_job_id = new_job_id
            status_description = f"Objects with ID {id_list} successfully deleted"
            status = HydraStatus(
                code=200, title="Objects successfully deleted", desc=status_description
            )
            return set_response_headers(jsonify(status.generate()))

        except (ClassNotFound, InstanceNotFound) as e:
            error = e.get_HTTP()
            return error_response(error)

    abort(405)


def items_delete_members_response(path: str, collection_id_: str, int_list="") -> Response:
    """
    Handles DELETE operation to insert multiple items.

    :param path: Path for Item Collection
    :type path: str
    :param collection_id_: ID of the collection
    :type collection_id_: str
    :param int_list: Optional String containing ',' separated ID's
    :type int_list: List
    :return: Appropriate response for the DELETE operation on multiple items.
    :rtype: Response
    """
    collections, parsed_classes = get_collections_and_parsed_classes()
    if path in parsed_classes:
            abort(405)
    if path in collections:
        item_class = collections[path]["collection"]
        class_type = item_class.name
        # Get path of the collection-class
        class_path = item_class.path
    if checkClassOp(class_path, "DELETE"):
        # Check if class_type supports PUT operation
        try:
            # Delete the Item with ID == id_
            crud.delete_multiple_members(collection_id_,
                                         int_list,
                                         class_type,
                                         session=get_session())
            id_list = int_list.split(',')
            status_description = f"Objects with ID {id_list} successfully deleted"
            status = HydraStatus(code=200,
                                 title="Objects successfully deleted",
                                 desc=status_description)
            return set_response_headers(jsonify(status.generate()))

        except (ClassNotFound, InstanceNotFound) as e:
            error = e.get_HTTP()
            return error_response(error)

    abort(405)
