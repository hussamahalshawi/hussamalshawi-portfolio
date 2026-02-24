import os
from datetime import datetime, timezone
import os
from flask_admin.form import ImageUploadField
from wtforms import MultipleFileField
from werkzeug.utils import secure_filename
from flask_admin.contrib.mongoengine import ModelView
from flask_admin.form import FileUploadField
from markupsafe import Markup
from config import Config
from flask import flash, redirect, url_for
from flask_admin.actions import action
from flask_admin import expose
from App.services.skill_service import SkillService
import logging
from flask import request

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
    form_overrides = {'profile_image': FileUploadField, 'profile_image2': FileUploadField}
    form_args = {
        'profile_image': {'label': 'Avatar Image',
                          'base_path': Config.UPLOAD_PATH,
                          'allow_overwrite': True},
        'profile_image2': {'label': 'Avatar Image2',
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


class ProjectView(ModelView):
    """
    إدارة مشاريع حسام: تتيح اختيار صور متعددة من الجهاز
    وتخزين مساراتها في ListField.
    """

    # 2. إضافة حقل اختيار الملفات من الجهاز (بدلاً من الكتابة اليدوية)
    form_extra_fields = {
        'image_selector': MultipleFileField('اختر صور المشروع من جهازك')
    }

    # 3. إخفاء حقل القائمة الأصلي لكي لا يظهر كصندوق نصي (String)
    form_excluded_columns = ['project_image']

    def on_model_change(self, form, model, is_created):
        """
        هذا الكود يعمل عند الضغط على Save:
        يأخذ الملفات من جهازك، يحفظها في المجلد، ويضع روابطها في الداتابيز.
        """
        # جلب الملفات المرفوعة من الحقل الإضافي 'image_selector'
        files = request.files.getlist('image_selector')

        # التأكد من أن المستخدم اختار ملفات فعلاً
        if files and files[0].filename != '':
            model.project_image = []

            for file in files:
                if file:
                    # تنظيف اسم الملف وحفظه في السيرفر المحلي
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(Config.UPLOAD_PATH, filename))

                    # حفظ المسار النسبي (Relative Path) لسهولة العرض بـ url_for
                    db_path = f"{Config.UPLOAD_PATH}/{filename}"

                    # إضافة المسار للقائمة (ListField)
                    if filename not in model.project_image:
                        model.project_image.append(filename)

        # ملاحظة: يمكنك إضافة دالة هنا لمسح الصور القديمة إذا أردت (اختياري)
        print(f"✅ تم رفع {len(model.project_image)} صور للمشروع بنجاح.")


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
    """
    Administrative view for Skill management.
    Features automated categorization synchronization and robust error handling.
    """

    # --- DISPLAY SETTINGS ---
    column_list = ('skill_name', 'skill_type', 'level', 'last_updated')
    column_labels = {
        'skill_name': 'Technical Skill',
        'skill_type': 'Category/Type',
        'level': 'Proficiency (%)',
        'last_updated': 'Last Sync'
    }

    # --- INTERFACE CONTROLS ---
    column_searchable_list = ('skill_name',)
    column_filters = ('skill_type', 'level')
    column_default_sort = ('level', True)  # Shows highest skills first

    # --- ACTIONS ---
    @action('update_skill_groups',
            'Sync Selected Types',
            'Are you sure you want to re-categorize the selected skills based on current Keyword logic?')
    def action_update_skills(self, ids):
        """
        Triggers the bulk update service for selected skills.
        Ensures the UI provides feedback on success or failure.
        """
        try:
            # Service call to perform logic (Separation of Concerns)
            count = SkillService.bulk_update_categories()

            if count > 0:
                flash(f'Success: {count} skills were re-mapped to their correct types.', 'success')
            else:
                flash('Sync complete. No changes were necessary for the selected skills.', 'info')

        except Exception as e:
            # Log the error for the developer and show a safe message to the admin
            logging.error(f"Admin Action Error: {str(e)}")
            flash(f'System Error: Could not complete synchronization. {str(e)}', 'error')

    # --- CUSTOM ROUTES ---
    @expose('/sync-all-types/')
    def sync_all_view(self):
        """
        A global sync route that can be triggered via a button in the UI.
        Redirects back to the list view after processing.
        """
        try:
            count = SkillService.bulk_update_categories()
            flash(f'Global Synchronization Complete: {count} skills updated.', 'info')
        except Exception as e:
            logging.error(f"Global Sync Error: {str(e)}")
            flash('A critical error occurred during global synchronization.', 'error')

        # Redirect back to the main list view to prevent page refresh re-submission
        return redirect(url_for('.index_view'))

    # --- FORMATTERS ---
    column_formatters = {
        'last_updated': lambda v, c, m, p: m.last_updated.strftime('%Y-%m-%d %H:%M') if m.last_updated else "N/A"
    }



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