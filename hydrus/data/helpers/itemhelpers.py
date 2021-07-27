"""Helper functions for items"""
import json

from flask import jsonify, request
from hydra_python_core.doc_writer import HydraStatus, HydraError

from hydrus.data import crud
from hydrus.data.exceptions import (
    ClassNotFound,
    InstanceNotFound,
    InstanceExists,
    InvalidDateTimeFormat,
    PropertyNotFound,
    MemberInstanceNotFound,
)
from hydrus.data.helpers import (
    set_response_headers,
    finalize_response,
    hydrafy,
    getType,
    send_sync_update,
    get_link_props,
    error_response,
    validate_object,
    parse_collection_members,
    get_collections_and_parsed_classes,
)
from hydrus.utils import get_session, get_api_name, get_hydrus_server_url, get_doc
from hydrus.extensions.socketio_factory import socketio


def items_get_check_support(id_, class_type, class_path, path, is_collection=False):
    """Check if class_type supports GET operation"""
    try:
        # Try getting the Item based on ID and Class type
        response = crud.get(
            id_,
            class_type,
            api_name=get_api_name(),
            session=get_session(),
            path=path,
            collection=is_collection,
        )

        response = finalize_response(class_path, response)
        return set_response_headers(jsonify(hydrafy(response, path=path)))

    except (ClassNotFound, InstanceNotFound) as e:
        error = e.get_HTTP()
        return error_response(error)


def items_post_check_support(id_, object_, class_path, path, is_collection):
    """Check if class_type supports POST operation"""
    collections, parsed_classes = get_collections_and_parsed_classes()
    doc = get_doc()
    if path in parsed_classes:
        class_path = path
        obj_type = getType(path, "PUT")
    elif path in collections:
        collection = collections[path]["collection"]
        class_path = collection.path
        obj_type = collection.name
    link_props, link_type_check = get_link_props(class_path, object_)
    # Load new object and type
    if validate_object(object_, obj_type, class_path) and link_type_check:
        if is_collection:
            object_ = parse_collection_members(object_)
        try:
            # Update the right ID if the object is valid and matches
            # type of Item
            object_id = crud.update(
                doc,
                object_=object_,
                id_=id_,
                type_=object_["@type"],
                session=get_session(),
                api_name=get_api_name(),
                collection=is_collection,
            )
            method = "POST"
            resource_url = (
                f"{get_hydrus_server_url()}{get_api_name()}/{path}/{object_id}"
            )
            last_job_id = crud.get_last_modification_job_id(session=get_session())
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
            headers_ = [{"Location": resource_url}]
            status_description = f"Object with ID {object_id} successfully " "updated"
            status = HydraStatus(
                code=200, title="Object updated", desc=status_description
            )
            status_response = status.generate()
            status_response["iri"] = resource_url
            return set_response_headers(jsonify(status_response), headers=headers_)

        except (ClassNotFound, InstanceNotFound, InstanceExists,
                PropertyNotFound, InvalidDateTimeFormat) as e:
            error = e.get_HTTP()
            return error_response(error)
    else:
        error = HydraError(code=400, title="Data is not valid")
        return error_response(error)


def items_put_check_support(id_, class_path, path, is_collection):
    """Check if class_type supports PUT operation"""
    object_ = json.loads(request.data.decode("utf-8"))
    doc = get_doc()
    collections, parsed_classes = get_collections_and_parsed_classes()
    if path in parsed_classes:
        class_path = path
        obj_type = getType(path, "PUT")
    elif path in collections:
        collection = collections[path]["collection"]
        class_path = collection.path
        obj_type = collection.name
    link_props, link_type_check = get_link_props(class_path, object_)
    # Load new object and type
    if validate_object(object_, obj_type, class_path) and link_type_check:
        if is_collection:
            object_ = parse_collection_members(object_)
        try:
            # Add the object with given ID
            object_id = crud.insert(
                doc,
                object_=object_,
                id_=id_,
                session=get_session(),
                collection=is_collection,
            )
            resource_url = (
                f"{get_hydrus_server_url()}{get_api_name()}/{path}/{object_id}"
            )
            headers_ = [{"Location": resource_url}]
            status_description = f"Object with ID {object_id} successfully added"
            status = HydraStatus(
                code=201, title="Object successfully added.", desc=status_description
            )
            status_response = status.generate()
            status_response["iri"] = resource_url
            return set_response_headers(
                jsonify(status_response), headers=headers_, status_code=status.code
            )
        except (ClassNotFound, InstanceExists,
                PropertyNotFound, InvalidDateTimeFormat) as e:
            error = e.get_HTTP()
            return error_response(error)
    else:
        error = HydraError(code=400, title="Data is not valid")
        return error_response(error)


def items_delete_check_support(id_, class_type, path, is_collection):
    """Check if class_type supports PUT operation"""
    try:
        # Delete the Item with ID == id_
        # for colletions, id_ is corresponding to their collection_id and not the id_
        # primary key
        crud.delete(id_, class_type, session=get_session(), collection=is_collection)
        method = "DELETE"
        resource_url = f"{get_hydrus_server_url()}{get_api_name()}/{path}/{id_}"
        last_job_id = crud.get_last_modification_job_id(session=get_session())
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
        status_description = f"Object with ID {id_} successfully deleted"
        status = HydraStatus(
            code=200, title="Object successfully deleted.", desc=status_description
        )
        return set_response_headers(jsonify(status.generate()))

    except (ClassNotFound, InstanceNotFound) as e:
        error = e.get_HTTP()
        return error_response(error)


def member_get_check_support(collection_id, member_id, class_type, class_path, path):
    """Check if class_type supports GET operation"""
    try:
        # Try getting the Item based on Collection ID and Member ID and Class type
        response = crud.get_member(
            collection_id,
            member_id,
            class_type,
            api_name=get_api_name(),
            session=get_session(),
            path=path,
        )

        response = finalize_response(class_path, response)
        return set_response_headers(jsonify(hydrafy(response, path=path)))

    except (ClassNotFound, MemberInstanceNotFound) as e:
        error = e.get_HTTP()
        return error_response(error)


def member_delete_check_support(collection_id, member_id, class_type, path):
    """Check if class_type supports DELETE operation"""
    try:
        # Delete the Item with IDs collection_id and member_id
        # collection_id is id of a collection
        # member_id is the id of member of a collection
        crud.delete_member(collection_id, member_id, class_type, session=get_session())

        method = "DELETE"
        resource_url = (
            f"{get_hydrus_server_url()}{get_api_name()}/{path}/{collection_id}"
        )
        last_job_id = crud.get_last_modification_job_id(session=get_session())
        new_job_id = crud.insert_modification_record(
            method, resource_url, session=get_session()
        )
        status_description = (
            f"Object with ID {member_id} successfully"
            f" deleted from Collection with ID {collection_id}"
        )
        status = HydraStatus(
            code=200, title="Object successfully deleted.", desc=status_description
        )
        return set_response_headers(jsonify(status.generate()))

    except (ClassNotFound, MemberInstanceNotFound) as e:
        error = e.get_HTTP()
        return error_response(error)
