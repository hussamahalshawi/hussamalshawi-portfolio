from flask import Flask
from flask_admin import Admin
from flask_admin.form import FileUploadField
from app.admin_views import ProfileView, EducationView, CourseView, ProjectView
from app.models.database import init_db
from config import Config
from app.routes import portfolio
from flask_admin.contrib.mongoengine import ModelView
from app.models import (
    Profile,
    Education,
    Course,
    Project,
)



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    admin = Admin(app, name='Hussam Portfolio Admin', url='/admin')
    admin.add_view(ProfileView(Profile, name='Profile'))
    admin.add_view(EducationView(Education, name='Education'))
    admin.add_view(CourseView(Course, name='Course'))
    admin.add_view(ProjectView(Project, name='Project'))
    init_db(app)

    app.register_blueprint(portfolio)

    return app