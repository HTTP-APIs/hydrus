from flask import Flask

app = Flask(__name__)

from thespian.actors import ActorSystem

def start_system():
    return ActorSystem()

system = None

from routes import *


if __name__ == '__main__':
    app.run()
    system = start_system()
