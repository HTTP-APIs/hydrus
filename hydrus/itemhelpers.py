"""Helper functions for items"""

from flask import jsonify

from hydrus.data import crud
from hydrus.data.exceptions import ClassNotFound, InstanceNotFound
from hydrus.helpers import set_response_headers, finalize_response, hydrafy
from hydrus.utils import get_session, get_api_name

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