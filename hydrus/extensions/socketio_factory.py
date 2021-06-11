from flask import Flask
from flask_socketio import SocketIO
from sqlalchemy.orm import scoped_session
from hydrus.extensions.sync_namespace import SyncNamespace


socketio = SocketIO()


def create_socket(app: Flask, session: scoped_session) -> SocketIO:
    socketio.init_app(app, logger=True)
    socketio.on_namespace(SyncNamespace(namespace='/sync', db_session=session))
    return socketio
