from typing import Union

from flask import jsonify, Response, request
from hydra_python_core.doc_writer import HydraError
from hydrus.utils import get_session, get_token, get_authentication

from hydrus.data.user import (create_nonce, check_authorization,
                              add_token, check_token)

from hydrus.helpers import set_response_headers


def token_response(token: str) -> Response:
    """
    Return succesful token generation object
    """
    message = {200: "User token generated"}
    response = set_response_headers(jsonify(message), status_code=200,
                                    headers=[{'X-Authorization': token}])
    return response


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
    response = set_response_headers(jsonify(message), status_code=401,
                                    headers=[{'WWW-Authenticate': realm},
                                             {'X-Authentication': nonce}])
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
        elif request.authorization is None:
            return failed_authentication(False)
        else:
            return verify_user()
    else:
        return None
