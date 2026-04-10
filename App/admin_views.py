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
from .utils import upload_media_to_cloud
import logging


# Setup local error logging
logger = logging.getLogger(__name__)

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
    """
    Admin View for Profile Management.
    Provides 5 dedicated file upload slots for the gallery.
    """
    column_list = ('full_name', 'title', 'last_updated')

    # تعريف حقول إضافية كأزرار رفع ملفات (ليست مربعات نص)
    extra_image_fields = {
        'img_slot_1': FileUploadField('Image 1', base_path=Config.UPLOAD_PATH),
        'img_slot_2': FileUploadField('Image 2', base_path=Config.UPLOAD_PATH),
        'img_slot_3': FileUploadField('Image 3', base_path=Config.UPLOAD_PATH),
        'img_slot_4': FileUploadField('Image 4', base_path=Config.UPLOAD_PATH),
        'img_slot_5': FileUploadField('Image 5', base_path=Config.UPLOAD_PATH),
    }

    # إضافة الحقول للنموذج
    form_extra_fields = extra_image_fields

    # تحديد ترتيب الحقول (إخفاء الحقل النصي الأصلي وإظهار الأزرار)
    form_columns = ('full_name', 'title', 'experience_years', 'overall_score', 'bio',
                    'linkedin_url', 'github_url', 'facebook_url', 'instagram_url',
                    'img_slot_1', 'img_slot_2', 'img_slot_3', 'img_slot_4', 'img_slot_5')

    def on_model_change(self, form, model, is_created):
        """
        Collects files from the slots and saves their Cloudinary URLs to profile_images list.
        """
        try:
            uploaded_urls = []

            # نمر على كل حقل من حقول الرفع الـ 5
            for i in range(1, 6):
                field_name = f'img_slot_{i}'
                file_data = request.files.get(field_name)

                if file_data and file_data.filename != '':
                    # إرجاع مؤشر الملف للبداية لضمان قراءة كاملة
                    file_data.seek(0)
                    # الرفع للسحاب (Cloudinary)
                    cloud_url = upload_media_to_cloud(file_data, folder_name="profile")
                    if cloud_url:
                        uploaded_urls.append(cloud_url)

            # إذا رفع المستخدم صوراً جديدة، نحدث القائمة
            if uploaded_urls:
                # يمكنك الإبقاء على الصور القديمة أو استبدالها، هنا سنستبدلها بالجديد
                model.profile_images = uploaded_urls

        except Exception as e:
            logger.error(f"Multi-upload failed: {str(e)}")
            flash(f"Error during image upload: {str(e)}", "error")

        return super(ProfileView, self).on_model_change(form, model, is_created)



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


class ProjectView(BaseSecureView):  # تأكد من الوراثة من BaseSecureView للأمان
    """
    إدارة مشاريع حسام: تتيح اختيار صور متعددة ورفعها مباشرة إلى Cloudinary.
    """
    column_list = ('project_name', 'project_type', 'last_updated')

    # 1. حقل اختيار ملفات متعددة من الجهاز
    form_extra_fields = {
        'image_selector': MultipleFileField('Upload Project Images to Cloud')
    }

    # 2. إخفاء الحقل النصي الأصلي (ListField) لضمان تجربة مستخدم نظيفة
    form_excluded_columns = ['project_image']

    def on_model_change(self, form, model, is_created):
        """
        عند الحفظ: يتم رفع الصور للسحاب وتخزين الروابط في مصفوفة project_image.
        """
        try:
            # جلب قائمة الملفات من الحقل الإضافي
            files = request.files.getlist('image_selector')

            # التحقق من وجود ملفات مختارة
            if files and any(f.filename != '' for f in files):
                # تفريغ القائمة القديمة إذا كنت تريد استبدال الصور بالكامل
                # أو يمكنك الإبقاء عليها والإضافة باستخدام append
                new_cloud_urls = []

                for file in files:
                    if file and file.filename != '':
                        try:
                            file.seek(0)
                            cloud_url = upload_media_to_cloud(file, folder_name="projects")

                            if cloud_url:
                                new_cloud_urls.append(cloud_url)
                            else:
                                # تسجيل الخطأ للملف المحدد فقط
                                logger.warning(f"⚠️ Skip: {file.filename} failed to upload.")

                        except Exception as file_error:
                            # منع انهيار العملية كاملة بسبب ملف واحد
                            logger.error(f"❌ Error uploading {file.filename}: {str(file_error)}")
                            continue
                # تحديث الموديل بالروابط السحابية الجديدة
                if new_cloud_urls:
                    model.project_image = new_cloud_urls
                    flash(f"Successfully uploaded {len(new_cloud_urls)} images to Cloudinary.", "success")

        except Exception as e:
            logger.error(f"Error in ProjectView (Cloud Upload): {str(e)}")
            flash(f"An error occurred: {str(e)}", "error")

        return super(ProjectView, self).on_model_change(form, model, is_created)

    # English Comment: This view overrides the local storage logic to stream
    # multiple files directly to Cloudinary and store the secure HTTPS URLs in MongoDB.

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


class LanguageView(BaseSecureView):
    column_list = ('language_name', 'level', 'last_updated')
    column_filters = ('level',)


class PostView(BaseSecureView):
    column_list = ('series', 'post_tags', 'is_published', 'created_at')
    # column_searchable_list = ('title', 'content')
    # column_filters = ('series', 'is_published')
    # form_widget_args = {'content': {'rows': 10, 'style': 'font-family: monospace;'}}
    # column_labels = {'post_tags': 'Required SEO Skills'}

class SeriesView(BaseSecureView):
    pass