from hydrus.application import app
from hydrus.handlers import *


app.add_url_rule('/api/<string:resource>', list_resources)
app.add_url_rule('/api', entrypoint)
