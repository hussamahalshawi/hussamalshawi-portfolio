import os
from datetime import datetime, timezone
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.form import FileUploadField
from flask import flash
from config import Config


# --- DESIGN PATTERN: BASE CLASS FOR ARCHITECTURAL INTEGRITY ---
class BaseSecureView(ModelView):
    """
    Standardizes behavior across all admin views.
    Ensures timestamps and validation are applied globally.
    """
    form_excluded_columns = ('last_updated',)
    column_display_pk = True  # Useful for debugging database IDs

    def on_model_change(self, form, model, is_created):
        """Automated UTC timestamping on save."""
        model.last_updated = datetime.now(timezone.utc)


# --- INDIVIDUAL MODEL VIEWS WITH FULL VALIDATION & UI CONFIG ---

class ProfileView(BaseSecureView):
    column_list = ('full_name', 'title', 'experience_years', 'overall_score')
    column_labels = {
        'full_name': 'Full Name',
        'title': 'Professional Title',
        'experience_years': 'Years of Exp',
        'overall_score': 'Master Score %'
    }
    form_overrides = {'profile_image': FileUploadField}
    form_args = {
        'profile_image': {
            'label': 'Profile Photo',
            'base_path': Config.UPLOAD_PATH,
            'allow_overwrite': True
        }
    }


class EducationView(BaseSecureView):
    column_list = ('institution', 'degree', 'major', 'start_date', 'end_date')
    column_searchable_list = ('institution', 'major', 'degree')
    column_filters = ('degree', 'start_date')
    column_labels = {
        'institution': 'University/School',
        'degree': 'Degree Level',
        'major': 'Field of Study'
    }


class CourseView(BaseSecureView):
    column_list = ('course_name', 'organization', 'start_date', 'acquired_skills')
    column_searchable_list = ('course_name', 'organization')
    column_filters = ('organization',)
    column_formatters = {
        'acquired_skills': lambda v, c, m, p: ", ".join(m.acquired_skills) if m.acquired_skills else "None"
    }
    column_labels = {
        'course_name': 'Course Name',
        'organization': 'Platform/Provider',
        'acquired_skills': 'Skills Tagged'
    }


class ProjectView(BaseSecureView):
    column_list = ('project_name', 'github_url', 'last_updated')
    column_searchable_list = ('project_name', 'description')
    column_filters = ('last_updated',)

    form_overrides = {
        'project_image': FileUploadField,
        'project_video': FileUploadField
    }
    form_args = {
        'project_image': {'base_path': Config.UPLOAD_PATH, 'allow_overwrite': True},
        'project_video': {'base_path': Config.UPLOAD_PATH, 'allow_overwrite': True}
    }
    column_labels = {
        'project_name': 'Project Title',
        'github_url': 'GitHub Link',
        'skills_used': 'Tech Stack'
    }


class SelfStudyView(BaseSecureView):
    column_list = ('title', 'platform_name', 'last_updated')
    column_searchable_list = ('title', 'platform_name')
    form_overrides = {
        'cover_image': FileUploadField,
        'sample_video': FileUploadField
    }
    form_args = {
        'cover_image': {'base_path': Config.UPLOAD_PATH},
        'sample_video': {'base_path': Config.UPLOAD_PATH}
    }


class ExperienceView(BaseSecureView):
    column_list = ('job_title', 'company_name', 'is_current', 'start_date')
    column_searchable_list = ('job_title', 'company_name')
    column_filters = ('is_current', 'company_name')

    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)
        # LOGIC VALIDATION: Ensure current job has no end_date
        if model.is_current:
            model.end_date = None


class AchievementView(BaseSecureView):
    column_list = ('title', 'issuing_organization', 'date_obtained')
    column_searchable_list = ('title', 'issuing_organization')
    column_labels = {'date_obtained': 'Earned On', 'skills_demonstrated': 'Skills Proven'}


class SkillTypeView(BaseSecureView):
    column_list = ('name', 'keywords')
    # Formatter to show keywords as a clean comma-separated list
    column_formatters = {
        'keywords': lambda v, c, m, p: ", ".join(m.keywords) if m.keywords else ""
    }


class SkillView(BaseSecureView):
    column_list = ('skill_name', 'skill_type', 'level', 'last_updated')
    column_searchable_list = ('skill_name',)
    column_filters = ('skill_type', 'level')
    # Level is capped at 95 visually but stored exactly
    column_labels = {'skill_name': 'Skill', 'level': 'Proficiency Level %'}


class GoalView(BaseSecureView):
    column_list = ('goal_name', 'target_score', 'current_score')
    column_labels = {'goal_name': 'Objective', 'required_skills': 'Linked Skills'}
    column_formatters = {
        'required_skills': lambda v, c, m, p: ", ".join(m.required_skills) if m.required_skills else ""
    }


class FeedbackView(BaseSecureView):
    column_list = ('client_name', 'company', 'rating', 'created_at')
    column_filters = ('rating', 'created_at')
    can_create = False  # Feedbacks usually come from the public site, not admin


class LanguageView(BaseSecureView):
    column_list = ('language', 'proficiency_level')
    column_choices = {
        'proficiency_level': [
            ('Native', 'Native'),
            ('Professional', 'Professional'),
            ('Elementary', 'Elementary')
        ]
    }


class PostView(BaseSecureView):
    """
    Blog Post View - Integrated with SEO rule support as per 2026 requirements.
    """
    column_list = ('title', 'series_type', 'is_published', 'created_at')
    column_searchable_list = ('title', 'content')
    column_filters = ('series_type', 'is_published')
    form_widget_args = {
        'content': {'rows': 10, 'style': 'font-family: monospace;'}
    }
    column_labels = {'series_type': 'Category/Series', 'is_published': 'Live on Site'}