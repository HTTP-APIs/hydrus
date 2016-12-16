from application import app
from server.handlers import *


app.add_url_rule('/api/available', 'available', list_resources)
app.add_url_rule('/api/<string:resource>', 'resources', read_resource)
app.add_url_rule('/api', 'root', entrypoint)
