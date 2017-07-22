import os


## Using sqlite as database
global DB_URL
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
DB_URL = 'sqlite:///{}'.format(db_path)


global HYDRUS_SERVER_URL, API_NAME, PORT
HYDRUS_SERVER_URL = "http://localhost:8080/"
PORT = 8080
API_NAME = "api"
