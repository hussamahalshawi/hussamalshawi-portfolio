from flask import Flask
from flask_admin import Admin
from flask_admin.form import FileUploadField
from App.admin_views import ProfileView, EducationView, CourseView, ProjectView, SelfStudyView, ExperienceView, AchievementView, SkillTypeView, SkillView, GoalView, FeedbackView, LanguageView, PostView
from App.models.database import init_db
from config import Config
from App.routes import portfolio
from flask_admin.contrib.mongoengine import ModelView
from App.models import (
    Profile,
    Education,
    Course,
    Project,
    SelfStudy,
    Experience,
    Achievement,
    SkillType,
    Skill,
    Goal,
    Feedback,
    Language,
    Post,
)



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    app.register_blueprint(portfolio)
    admin = Admin(app, name='Hussam Portfolio Admin', url='/admin')
    admin.add_view(ProfileView(Profile, name='Profile'))
    admin.add_view(EducationView(Education, name='Education'))
    admin.add_view(CourseView(Course, name='Course'))
    admin.add_view(ProjectView(Project, name='Project'))
    admin.add_view(SelfStudyView(SelfStudy, name='SelfStudy'))
    admin.add_view(ExperienceView(Experience, name='Experience'))
    admin.add_view(AchievementView(Achievement, name='Achievement'))
    admin.add_view(SkillTypeView(SkillType, name='SkillType'))
    admin.add_view(SkillView(Skill, name='Skill'))
    admin.add_view(GoalView(Goal, name='Goal'))
    admin.add_view(FeedbackView(Feedback, name='Feedback'))
    admin.add_view(LanguageView(Language, name='Language'))
    admin.add_view(PostView(Post, name='Post'))

    with app.app_context():
        try:
            import App.signals
        except ImportError as e:
            App.logger.error(f"Could not import signals: {e}")

    return app