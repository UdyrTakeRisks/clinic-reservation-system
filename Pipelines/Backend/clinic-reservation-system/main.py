from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)  # flask app object
    CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})
    return app
