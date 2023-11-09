from flask import Flask


def create_app():
    app = Flask(__name__)  # flask app object

    return app


