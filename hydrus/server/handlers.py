"""
Handlers for the Flask server.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from flask import jsonify, request
from data.apidocumentation import global_doc, make_doc

def entrypoint():
    """
    Return a set of URI
    """
    return jsonify({
        "collections": ["/api/astronomy", "/api/solarsystem"], 
        "hydra:apiDocumentation": "/api/hydra",  # link to global documentation
        "resources": "/api/<class>",  # list possible classes
        "documentation": "/api/hydra/<view>"  # list routes' documentation
    })

def hydra_documentation(view=None):
    """
    Return HYDRA apiDocumentation for given view.

    :view str: the name given to the route in routes.py
    """
    if view is None: return jsonify(global_doc)

    return jsonify(make_doc(view))

def list_resources():
    """
    Provide the list of resources
    """

    # load vocabulary in data/ to create an array of allowed names
    from server.parser import collect_astronomy_resources
    try:
        ALLOWED_RESOURCES = collect_astronomy_resources(request.url_rule.endpoint)
    except AttributeError as e:
        return jsonify({"error": 1})

    return jsonify(ALLOWED_RESOURCES)

def read_resources(resource):
    """
    Provide a collection of `owl:Class`
    """

    return jsonify({
        "resource": resource
    })

def crud_resource(resource, crud, id_=None):
    """
    Provide a CRUD operation on a particular resource
    """
    if crud not in ['create', 'read', 'update', 'delete']: return jsonify({"error": 1})

    if crud == 'read' and id_ == None: return jsonify({"error": 1})

    # if crud == 'read' and id_ is hexdigest: resource lookup by hash

    return jsonify({
        "resource": resource,
        "operation": crud
    })

