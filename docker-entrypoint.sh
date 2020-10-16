#!/bin/sh

set -e

. /.venv/bin/activate

# exec uwsgi --http :8080 --wsgi-file hydrus/app.py

exec uwsgi --http :8080 hydrus/uwsgi.ini