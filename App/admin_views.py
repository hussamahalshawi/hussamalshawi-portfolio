import os
from datetime import datetime, timezone
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.form import FileUploadField
from markupsafe import Markup
from config import Config


# --- DESIGN PATTERN: BASE CLASS FOR SYSTEM INTEGRITY ---
class BaseSecureView(ModelView):
    """
    Standardizes behavior across all admin views.
    Enforces security, auditing, and clean list formatting.
    """
    form_excluded_columns = ('last_updated',)
    column_display_pk = True

    # MASTER FORMATTER: Handles all variations of skill lists across models
    column_formatters = {
        'skills_learned': lambda v, c, m, p: ", ".join(m.skills_learned) if hasattr(m,
                                                                                    'skills_learned') and m.skills_learned else "None",
        'skills_used': lambda v, c, m, p: ", ".join(m.skills_used) if hasattr(m,
                                                                              'skills_used') and m.skills_used else "None",
        'acquired_skills': lambda v, c, m, p: ", ".join(m.acquired_skills) if hasattr(m,
                                                                                      'acquired_skills') and m.acquired_skills else "None",
        'skills_acquired': lambda v, c, m, p: ", ".join(m.skills_acquired) if hasattr(m,
                                                                                      'skills_acquired') and m.skills_acquired else "None",
        'skills_demonstrated': lambda v, c, m, p: ", ".join(m.skills_demonstrated) if hasattr(m,
                                                                                              'skills_demonstrated') and m.skills_demonstrated else "None",
        'required_skills': lambda v, c, m, p: ", ".join(m.required_skills) if hasattr(m,
                                                                                      'required_skills') and m.required_skills else "None",
        'post_tags': lambda v, c, m, p: ", ".join(m.post_tags) if hasattr(m, 'post_tags') and m.post_tags else "None"
    }

    def on_model_change(self, form, model, is_created):
        """Ensures every save action is timestamped in UTC."""
        model.last_updated = datetime.now(timezone.utc)


# --- INDIVIDUAL MODEL VIEWS WITH FULL DETAILS ---

class ProfileView(BaseSecureView):
    column_list = ('full_name', 'title', 'experience_years', 'overall_score', 'last_updated')
    column_labels = {
        'full_name': 'Full Name',
        'experience_years': 'Years of Exp',
        'overall_score': 'Master Score %'
    }
    form_overrides = {'profile_image': FileUploadField}
    form_args = {
        'profile_image': {'label': 'Avatar Image',
                          'base_path': Config.UPLOAD_PATH,
                          'allow_overwrite': True}
    }


class EducationView(BaseSecureView):
    column_list = ('institution', 'degree', 'major', 'skills_learned', 'start_date', 'end_date')
    column_searchable_list = ('institution', 'major', 'degree')
    column_filters = ('degree', 'start_date')
    column_labels = {'skills_learned': 'Required Skills'}


class CourseView(BaseSecureView):
    column_list = ('course_name', 'organization', 'acquired_skills', 'start_date')
    column_searchable_list = ('course_name', 'organization')
    column_filters = ('organization',)
    column_labels = {'acquired_skills': 'Required Skills'}


class ProjectView(BaseSecureView):
    column_list = ('project_name', 'category', 'github_url', 'skills_used')
    column_filters = ('category', 'last_updated')  # This creates a dropdown filter in Admin
    column_searchable_list = ('project_name', 'description')

    form_overrides = {'project_image': FileUploadField, 'project_video': FileUploadField}
    form_args = {
        'project_image': {'base_path': Config.UPLOAD_PATH, 'allow_overwrite': True},
        'project_video': {'base_path': Config.UPLOAD_PATH, 'allow_overwrite': True}
    }

class CategoryView(BaseSecureView):
    column_list = ('name', 'description', 'created_at')
    column_searchable_list = ('name',)

class SelfStudyView(BaseSecureView):
    column_list = ('title', 'platform_name', 'skills_learned', 'last_updated')
    column_searchable_list = ('title', 'platform_name')
    column_labels = {'skills_learned': 'Required Skills'}
    form_overrides = {'cover_image': FileUploadField, 'sample_video': FileUploadField}
    form_args = {
        'cover_image': {'base_path': Config.UPLOAD_PATH},
        'sample_video': {'base_path': Config.UPLOAD_PATH}
    }


class ExperienceView(BaseSecureView):
    column_list = ('job_title', 'company_name', 'is_current', 'skills_acquired')
    column_searchable_list = ('job_title', 'company_name')
    column_filters = ('is_current', 'company_name')
    column_labels = {'skills_acquired': 'Required Skills'}

    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)
        if model.is_current:
            model.end_date = None


class AchievementView(BaseSecureView):
    column_list = ('title', 'issuing_organization', 'skills_demonstrated', 'date_obtained')
    column_searchable_list = ('title', 'issuing_organization')
    column_labels = {'skills_demonstrated': 'Required Skills'}


class SkillTypeView(BaseSecureView):
    column_list = ('name', 'keywords')
    column_searchable_list = ('name',)


class SkillView(BaseSecureView):
    column_list = ('skill_name', 'skill_type', 'level', 'last_updated')
    column_searchable_list = ('skill_name',)
    column_filters = ('skill_type', 'level')


class GoalView(BaseSecureView):
    """
    Administrative interface for managing career goals.
    Features automated score synchronization and read-only progress metrics.
    """

    # --- DISPLAY CONFIGURATION ---
    # Defines columns visible in the main list view
    column_list = [
        'goal_name',
        'target_year',
        'current_score',
        'target_score',
        'last_updated'
    ]

    # Custom labels for better UI clarity
    column_labels = {
        'goal_name': 'Goal Milestone',
        'target_year': 'Target Year',
        'current_score': 'Current Progress',
        'target_score': 'Success Threshold',
        'last_updated': 'Last Synced'
    }

    # --- SEARCH & FILTERING ---
    column_searchable_list = ('goal_name', 'sub_title')
    column_filters = ('target_year', 'current_score')
    column_default_sort = ('target_year', False)

    # --- FORM CUSTOMIZATION ---
    # Prevents manual tampering with auto-calculated fields
    form_widget_args = {
        'current_score': {'readonly': True},
        'last_updated': {'readonly': True}
    }

    # --- FORMATTERS ---
    column_formatters = {
        'last_updated': lambda v, c, m, p: m.last_updated.strftime('%Y-%m-%d %H:%M') if m.last_updated else "Never",
        'current_score': lambda v, c, m, p: Markup(f"<b>{m.current_score}%</b>")
    }

    def on_model_change(self, form, model, is_created):
        """
        Event hook triggered before saving a document.
        Ensures the score is synchronized with the latest skill levels.
        """
        try:
            # Update the timestamp using a timezone-aware object
            model.last_updated = datetime.now(timezone.utc)

            # Trigger the internal synchronization logic defined in the Model
            # This ensures the score reflects the actual skill proficiency
            model.sync_with_existing_skills()

        except Exception as e:
            # Standard error handling logic for Admin interfaces
            raise Exception(f"Failed to synchronize goal data: {str(e)}")


class FeedbackView(BaseSecureView):
    column_list = ('person_name', 'job_title', 'contact_email', 'created_at')
    column_searchable_list = ('person_name', 'feedback_text')
    can_create = False  # Testimonials are usually submitted via public form


class LanguageView(BaseSecureView):
    column_list = ('language_name', 'level', 'last_updated')
    column_filters = ('level',)


class PostView(BaseSecureView):
    column_list = ('title', 'series', 'post_tags', 'is_published', 'created_at')
    column_searchable_list = ('title', 'content')
    column_filters = ('series', 'is_published')
    form_widget_args = {'content': {'rows': 10, 'style': 'font-family: monospace;'}}
    column_labels = {'post_tags': 'Required SEO Skills'}