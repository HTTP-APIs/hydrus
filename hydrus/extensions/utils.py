import socketio

from hydrus.extensions.sync_namespace import send_sync_update
from hydrus import crud
from hydrus.utils import (
    get_hydrus_server_url,
    get_api_name,
    get_session
)


def send_update(method: str, path: str):
    """Handler for sending synchronization update to all connected clients.

    :param method: Method type of the operation.
    :type method: str
    :param path: Path to the Item collection to which update is made.
    :type path: str
    """
    resource_url = f"{get_hydrus_server_url()}{get_api_name()}/{path}"
    session = get_session()
    last_job_id = crud.get_last_modification_job_id(session)
    new_job_id = crud.insert_modification_record(method, resource_url, session)
    send_sync_update(socketio, new_job_id, last_job_id, method, resource_url)
