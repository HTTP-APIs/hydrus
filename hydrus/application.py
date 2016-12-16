from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True

from thespian.actors import ActorSystem

def start_system():
    return ActorSystem()

from server.routes import *


if __name__ == '__main__':
    app.run()
    start_system()
