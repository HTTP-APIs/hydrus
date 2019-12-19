from typing import Union
import json
from flask import jsonify, Response, request, redirect, url_for
from hydra_python_core.doc_writer import HydraError
from hydrus.utils import get_session, get_token, get_authentication

from hydrus.data.user import (create_nonce, check_authorization, vague_Response,
                              add_token, check_token, check_nonce)

from hydrus.helpers import set_response_headers


def token_response(token: str) -> Response:
    """
    Return succesful token generation object
    """
    resp = Response()
    resp.response = json.dumps({"message": "tokengranted"})
    resp.set_cookie("nonce", token)
    resp.status_code = 200
    return resp


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
    response = Response()
    response.response = json.dumps(message)
    response.set_cookie("nonce", nonce)
    response.headers["WWW-Authenticate"] = realm
    response.status_code = 401
    return response


def verify_user() -> Union[Response, None]:
    """
    Verify the credentials of the user and assign token.
    """
    try:
        auth = check_authorization(request, get_session())
        if auth is False:
            return failed_authentication(True)
        elif get_token():
            token = add_token(request, get_session())
            return token_response(token)
    except Exception as e:
        error = e.get_HTTP()  # type: HydraError
        return set_response_headers(jsonify(error.generate()), status_code=error.code)
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
            return None
        elif request.authorization is None:
            return failed_authentication(False)
        else:
            return verify_user()
    else:
        return None
