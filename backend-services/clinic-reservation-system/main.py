from flask import Flask


# from flask_cors import CORS, cross_origin

def create_app():
    app = Flask(__name__)  # flask app object
    # CORS(app)
    return app
