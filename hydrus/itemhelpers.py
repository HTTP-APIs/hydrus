"""Helper functions for items"""
import json

from flask import jsonify, request
from hydra_python_core.doc_writer import HydraStatus, HydraError

from hydrus.data import crud
from hydrus.data.exceptions import (
    ClassNotFound,
    InstanceNotFound,
    InstanceExists,
    PropertyNotFound)
from hydrus.helpers import (
    set_response_headers,
    finalize_response,
    hydrafy,
    getType,
    validObject,
    check_required_props,
    send_sync_update,
    get_link_props,
    error_response,
    validate_object)
from hydrus.utils import (
    get_session,
    get_api_name,
    get_hydrus_server_url)
from hydrus.socketio_factory import socketio


def items_get_check_support(id_, class_type, class_path, path):
    """Check if class_type supports GET operation"""
    try:
        # Try getting the Item based on ID and Class type
        response = crud.get(
            id_,
            class_type,
            api_name=get_api_name(),
            session=get_session())

        response = finalize_response(class_path, response)
        return set_response_headers(
            jsonify(hydrafy(response, path=path)))

    except (ClassNotFound, InstanceNotFound) as e:
        error = e.get_HTTP()
        return error_response(error)


def items_post_check_support(id_, object_, class_path, path):
    """Check if class_type supports POST operation"""
    obj_type = getType(class_path, "POST")
    link_props, link_type_check = get_link_props(class_path, object_)
    # Load new object and type
    if (validate_object(object_, obj_type, class_path) and link_type_check):
        try:
            # Update the right ID if the object is valid and matches
            # type of Item
            object_id = crud.update(
                object_=object_,
                id_=id_,
                link_props=link_props,
                type_=object_["@type"],
                session=get_session(),
                api_name=get_api_name())
            method = "POST"
            resource_url = "{}{}/{}/{}".format(
                get_hydrus_server_url(), get_api_name(), path, object_id)
            last_job_id = crud.get_last_modification_job_id(
                session=get_session())
            new_job_id = crud.insert_modification_record(method, resource_url,
                                                         session=get_session())
            send_sync_update(socketio=socketio, new_job_id=new_job_id,
                             last_job_id=last_job_id, method=method,
                             resource_url=resource_url)
            headers_ = [{"Location": resource_url}]
            status_description = ("Object with ID {} successfully "
                                  "updated").format(object_id)
            status = HydraStatus(
                code=200, title="Object updated", desc=status_description)
            return set_response_headers(jsonify(status.generate()),
                                        headers=headers_)

        except (ClassNotFound,
                InstanceNotFound,
                InstanceExists,
                PropertyNotFound
                ) as e:
            error = e.get_HTTP()
            return error_response(error)
    else:
        error = HydraError(code=400, title="Data is not valid")
        return error_response(error)


def items_put_check_support(id_, class_path, path):
    """Check if class_type supports PUT operation"""
    object_ = json.loads(request.data.decode('utf-8'))
    obj_type = getType(class_path, "PUT")
    link_props, link_type_check = get_link_props(class_path, object_)
    # Load new object and type
    if (validate_object(object_, obj_type, class_path) and link_type_check):
        try:
            # Add the object with given ID
            object_id = crud.insert(object_=object_, id_=id_,
                                    link_props=link_props,
                                    session=get_session())
            headers_ = [{"Location": "{}{}/{}/{}".format(
                get_hydrus_server_url(), get_api_name(), path, object_id)}]
            status_description = "Object with ID {} successfully added".format(
                object_id)
            status = HydraStatus(code=201, title="Object successfully added.",
                                 desc=status_description)
            return set_response_headers(
                jsonify(status.generate()), headers=headers_,
                status_code=status.code)
        except (ClassNotFound, InstanceExists, PropertyNotFound) as e:
            error = e.get_HTTP()
            return error_response(error)
    else:
        error = HydraError(code=400, title="Data is not valid")
        return error_response(error)


def items_delete_check_support(id_, class_type, path):
    """Check if class_type supports PUT operation"""
    try:
        # Delete the Item with ID == id_
        crud.delete(id_, class_type, session=get_session())
        method = "DELETE"
        resource_url = "{}{}/{}/{}".format(
            get_hydrus_server_url(), get_api_name(), path, id_)
        last_job_id = crud.get_last_modification_job_id(session=get_session())
        new_job_id = crud.insert_modification_record(method, resource_url,
                                                     session=get_session())
        send_sync_update(socketio=socketio, new_job_id=new_job_id,
                         last_job_id=last_job_id, method=method,
                         resource_url=resource_url)
        status_description = "Object with ID {} successfully deleted".format(
            id_)
        status = HydraStatus(code=200, title="Object successfully deleted.",
                             desc=status_description)
        return set_response_headers(jsonify(status.generate()))

    except (ClassNotFound, InstanceNotFound) as e:
        error = e.get_HTTP()
        return error_response(error)
