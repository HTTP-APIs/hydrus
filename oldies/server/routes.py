from application import app
from server.handlers import *


# check the documentation in the handlers.py

#
# generical collections based on initial ontologies
#

# ontology for general classes
app.add_url_rule('/api/astronomy', 'astronomy', list_resources, methods=['GET'])
# ontology for Solar System bodies
app.add_url_rule('/api/solarsystem', 'solarsystem', list_resources, methods=['GET'])


# routes to resources
app.add_url_rule('/api/<string:resource>/<string:crud>', 'crud_resources', crud_resource, methods=['POST', 'PUT'])
app.add_url_rule('/api/<string:resource>', 'resources', read_resources, methods=['POST', 'PUT'])


# routes to documentation
app.add_url_rule('/api/hydraspec/<string:view>', 'hydradoc_root', hydra_documentation, methods=['GET'])
app.add_url_rule('/api/hydraspec', 'hydradoc', hydra_documentation, methods=['GET'])


# route to entrypoint
app.add_url_rule('/api', 'root', entrypoint, methods=['GET'])
