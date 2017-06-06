"""Main route for the applciation."""

# Write code for views and API here.
from flask import Flask, jsonify, redirect, request
from flask_restful import Api, Resource
import json
from models import engine
from sqlalchemy import text


# from flask_cors import CORS, cross_origin

app = Flask(__name__)
api = Api(app)


def set_response_headers(resp, ct="application/json", status_code=200):
    """ Sets the response headers
        Default : { Content-type:"JSON-LD", status_code:200}"""
    resp.status_code = status_code
    resp.headers['Content-type'] = ct
    return resp


class Index(Resource):

    def get(self):
        """ Returns main entrypoint for the api."""
        # return set_response_headers(jsonify(entrypoint), 'application/ld+json', 200)
        pass

api.add_resource(Index, "/api", endpoint="api")

class Cots(Resource):
    """ Handles all operations(GET, POST, PATCH, DELETE) on
    Commercial Off The Shelves (COTS) spare parts for pico- and nano-satellites."""

    def get(self, id):
        query = text('select * from graph;')
        result = engine.execute(query)
        names = []
        for row in result:
            names.append(row)
        # print(jsonify(names))
        return names
    def post(self, id):
        pass

    def patch(self, id):
        pass

    def delete(self, id):
        pass

api.add_resource(Cots, "/api/cots/<string:id>", endpoint="cots")



class Spacecraft(Resource):
    """ Handles all operations(GET, POST, PATCH, DELETE) on Spacecrafts """

    def get(self, id):
        pass

    def post(self, id):
        pass

    def patch(self, id):
        pass

    def delete(self, id):
        pass

api.add_resource(Spacecraft, "/api/spacecraft/<string:id>", endpoint="spacecraft")


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=8080)
