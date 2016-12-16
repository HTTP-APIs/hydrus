"""
Handlers for the Flask server.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import jsonify

def entrypoint():
    """
    Return a set of URI
    """
    return jsonify({
        'root': '/api/',
        'allowed': '/api/available'
        })


def list_resources():
    """
    Provide the list of resources
    """

    # load vocabulary in data/ to create an array of allowed names
    from server.parser import collect_astronomy_resources
    ALLOWED_RESOURCES = collect_astronomy_resources()

    return jsonify({
        'available': ALLOWED_RESOURCES
    })

def read_resource(resource):
    """
    Provide the READ operation on resource
    """

    return jsonify({
        'resource': resource
    })


