from flask import Flask
from flask_login import LoginManager

from config import Config
from app.routes import portfolio


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    app.register_blueprint(portfolio)

    return app