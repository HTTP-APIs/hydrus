
def entrypoint():
    """
    Return a set of URI
    """
    return jsonify({})


def list_resources(resource):
    """
    Provide the READ operation on resource
    """
    return jsonify({'resource': resource})


