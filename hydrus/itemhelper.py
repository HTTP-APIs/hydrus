

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
    InvalidSearchParameter,
    OffsetOutOfRange)
from hydrus.helpers import (
    set_response_headers,
    checkClassOp,
    getType,
    validObject,
    checkEndpoint,
    validObjectList,
    type_match,
    hydrafy,
    check_writeable_props,
    check_required_props,
    add_iri_template,
    finalize_response,
    send_sync_update,
    get_link_props,
    get_link_props_for_multiple_objects)
from hydrus.utils import (
    get_session,
    get_doc,
    get_api_name,
    get_hydrus_server_url,
    get_page_size,
    get_pagination)
from hydrus.socketio_factory import socketio


def items_get_check_support(class_type,class_path,path,id_):
   
 
            # Check if class_type supports GET operation
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
                return set_response_headers(jsonify(error.generate()), status_code=error.code)


def items_post_check_support(class_path, object_, id_, path ):

        # Check if class_type supports POST operation
            obj_type = getType(class_path, "POST")
            link_props, link_type_check = get_link_props(class_path, object_)
            # Load new object and type
            if validObject(object_) and object_["@type"] == obj_type and check_required_props(
                    class_path, object_) and link_type_check:
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
                    last_job_id = crud.get_last_modification_job_id(session=get_session())
                    new_job_id = crud.insert_modification_record(method, resource_url,
                                                                 session=get_session())
                    send_sync_update(socketio=socketio, new_job_id=new_job_id,
                                     last_job_id=last_job_id, method=method,
                                     resource_url=resource_url)
                    headers_ = [{"Location": resource_url}]
                    status_description = "Object with ID {} successfully updated".format(object_id)
                    status = HydraStatus(code=200, title="Object updated", desc=status_description)
                    return set_response_headers(jsonify(status.generate()), headers=headers_)

                except (ClassNotFound, InstanceNotFound, InstanceExists, PropertyNotFound) as e:
                    error = e.get_HTTP()
                    return set_response_headers(jsonify(error.generate()), status_code=error.code)
            else:
                error = HydraError(code=400, title="Data is not valid")
                return set_response_headers(jsonify(error.generate()), status_code=error.code)



def items_put_check_support(class_path, id_, path):

     # Check if class_type supports PUT operation
            object_ = json.loads(request.data.decode('utf-8'))
            obj_type = getType(class_path, "PUT")
            link_props, link_type_check = get_link_props(class_path, object_)
            # Load new object and type
            if validObject(object_) and object_["@type"] == obj_type and check_required_props(
                    class_path, object_) and link_type_check:
                try:
                    # Add the object with given ID
                    object_id = crud.insert(object_=object_, id_=id_,
                                            link_props=link_props, session=get_session())
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


def items_delete_check_support(id_, class_type, path):

             # Check if class_type supports DELETE operation
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
                status_description = "Object with ID {} successfully deleted".format(id_)
                status = HydraStatus(code=200, title="Object successfully deleted.",
                                     desc=status_description)
                return set_response_headers(jsonify(status.generate()))

            except (ClassNotFound, InstanceNotFound) as e:
                error = e.get_HTTP()
                return set_response_headers(jsonify(error.generate()), status_code=error.code)

def get_(collection,path,search_params,class_path):
            try:
                # Get collection details from the database
                if get_pagination():
                    # Get paginated response
                    response = crud.get_collection(
                        get_api_name(), collection.class_.title, session=get_session(),
                        paginate=True, path=path, page_size=get_page_size(),
                        search_params=search_params)
                else:
                    # Get whole collection
                        response = crud.get_collection(
                        get_api_name(), collection.class_.title, session=get_session(),
                        paginate=False, path=path, search_params=search_params)

                response["search"] = add_iri_template(path=class_path,
                                                      API_NAME=get_api_name())

                return set_response_headers(jsonify(hydrafy(response, path=path)))

            except (ClassNotFound, PageNotFound, InvalidSearchParameter, OffsetOutOfRange) as e:
                error = e.get_HTTP()
                return set_response_headers(jsonify(error.generate()), status_code=error.code)


