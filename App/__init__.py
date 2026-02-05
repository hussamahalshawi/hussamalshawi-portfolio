import logging
from flask import Flask
from flask_admin import Admin
from config import Config
from App.routes import portfolio
from App.models.database import init_db
from App.admin_views import (
    ProfileView, EducationView, CourseView, ProjectView,
    SelfStudyView, ExperienceView, AchievementView,
    SkillTypeView, SkillView, GoalView, FeedbackView,
    LanguageView, PostView, CategoryView,
)
from App.models import (
    Profile, Education, Course, Project, SelfStudy,
    Experience, Achievement, SkillType, Skill,
    Goal, Feedback, Language, Post, Category
)


def configure_admin(app):
    """
    Initializes Flask-Admin and registers all model views.
    Enforces centralized administration management.
    """
    admin = Admin(app, name='Hussam Portfolio Admin', url='/admin')

    # Validation: Ensure all views are associated with their respective models correctly
    try:
        admin.add_view(ProfileView(Profile, name='Profile'))
        admin.add_view(EducationView(Education, name='Education'))
        admin.add_view(CourseView(Course, name='Course'))
        admin.add_view(ProjectView(Project, name='Project'))
        admin.add_view(CategoryView(Category, name='Category'))
        admin.add_view(SelfStudyView(SelfStudy, name='Self-Study'))
        admin.add_view(ExperienceView(Experience, name='Experience'))
        admin.add_view(AchievementView(Achievement, name='Achievement'))
        admin.add_view(SkillTypeView(SkillType, name='Skill Categories'))
        admin.add_view(SkillView(Skill, name='Skills Inventory'))
        admin.add_view(GoalView(Goal, name='Goals & Progress'))
        admin.add_view(FeedbackView(Feedback, name='Feedback'))
        admin.add_view(LanguageView(Language, name='Language Proficiency'))
        admin.add_view(PostView(Post, name='Blog Posts'))
    except Exception as admin_error:
        app.logger.error(f"[-] Admin Interface Registration Error: {admin_error}")


def create_app():
    """
    HussamAlshawi-Portfolio Application Factory.
    Implements full validation, modern logging, and design pattern standards.
    """
    app = Flask(__name__)

    # 1. Configuration Validation
    try:
        app.config.from_object(Config)
        # Ensure SECRET_KEY is set for session security
        if not app.config.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY must be configured in the environment.")
    except Exception as config_err:
        app.logger.critical(f"[-] Configuration Initialization Failed: {config_err}")
        raise

    # 2. Database Initialization with Integrity Check
    try:
        init_db(app)
    except Exception as db_err:
        app.logger.critical(f"[-] Database Connection Error: {db_err}")
        raise

    # 3. Blueprint Registration
    app.register_blueprint(portfolio)

    # 4. Admin Interface Setup
    configure_admin(app)

    # 5. Strategic Signal Registration (Crucial for Real-time Skill Sync)
    # Using app_context to ensure signals have access to the current app instance
    with app.app_context():
        try:
            import App.signals
            app.logger.info("[+] System signals synchronized successfully.")
        except ImportError as signal_err:
            app.logger.error(f"[-] Signal Import Failed: {signal_err}. Automation logic may be disabled.")
        except Exception as unexpected_err:
            app.logger.error(f"[-] Unexpected Signal Error: {unexpected_err}")

    # Final Verification: Log successful startup
    app.logger.info("🚀 HussamAlshawi-Portfolio App Factory started successfully.")

    return app