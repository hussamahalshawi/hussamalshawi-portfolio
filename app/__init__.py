from flask import Flask
from flask_admin import Admin
from flask_admin.form import FileUploadField
from app.admin_views import ProfileView
from app.models.database import init_db
from config import Config
from app.routes import portfolio
from flask_admin.contrib.mongoengine import ModelView
from app.models import (
    Profile
)



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    admin = Admin(app, name='Hussam Portfolio Admin', url='/admin')
    admin.add_view(ProfileView(Profile, name='Profile'))
    init_db(app)

    app.register_blueprint(portfolio)

    return app