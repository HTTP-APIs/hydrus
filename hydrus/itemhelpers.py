"""Helper functions for items"""

from flask import jsonify
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
    get_link_props)
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
        return set_response_headers(jsonify(error.generate()),
                                    status_code=error.code)


def items_post_check_support(id_, object_, class_path, path):
    """Check if class_type supports POST operation"""
    obj_type = getType(class_path, "POST")
    link_props, link_type_check = get_link_props(class_path, object_)
    # Load new object and type
    if (validObject(object_)
        and object_["@type"] == obj_type
        and check_required_props(class_path, object_)
            and link_type_check):
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
            return set_response_headers(jsonify(error.generate()),
                                        status_code=error.code)
    else:
        error = HydraError(code=400, title="Data is not valid")
        return set_response_headers(jsonify(error.generate()),
                                    status_code=error.code)
