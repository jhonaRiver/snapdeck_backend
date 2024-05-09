from flask import Flask
from flask_cors import CORS
from app.routes import app_blueprint


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(app_blueprint)
    return app
