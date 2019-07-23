from flask import Flask
from flask_socketio import SocketIO, Namespace


class SyncNamespace(Namespace):
    def on_connect(self):
        print("A Client connected")

    def on_disconnect(self):
        print("A client disconnected")


socketio = SocketIO()


def create_socket(app: Flask) -> SocketIO:
    socketio.init_app(app, logger=True)
    socketio.on_namespace(SyncNamespace('/sync'))
    return socketio
