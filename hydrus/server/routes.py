from application import app
from server.handlers import *


# check the documentation in the views
app.add_url_rule('/api/available', 'available', list_resources, method=['GET'])
app.add_url_rule('/api/<string:resource>', 'resources', read_resource, method=['POST', 'PUT'])
app.add_url_rule('/api/<string:resource>/<string:crud>', 'crud_resources', crud_resources, method=['POST', 'PUT'])
app.add_url_rule('/api', 'root', entrypoint, , method=['GET'])
