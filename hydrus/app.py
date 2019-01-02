"""Main route for the application"""

from hydrus.app_factory import app_factory


if __name__ == "__main__":

    app = app_factory("api")
    app.run(host='127.0.0.1', debug=True, port=8080)
