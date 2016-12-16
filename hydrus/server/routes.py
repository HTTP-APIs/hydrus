from application import app
from server.handlers import *


# check the documentation in the views
app.add_url_rule('/api/available', 'available', list_resources, methods=['GET'])
app.add_url_rule('/api/<string:resource>', 'resources', read_resources, methods=['POST', 'PUT'])
app.add_url_rule('/api/<string:resource>/<string:crud>', 'crud_resources', crud_resource, methods=['POST', 'PUT'])
app.add_url_rule('/api', 'root', entrypoint, methods=['GET'])
