import os
from datetime import datetime, timezone

from flask_admin.contrib.mongoengine import ModelView
from flask_admin.form import FileUploadField
from config import Config


class ProfileView(ModelView):
    column_list = ('full_name', 'title', 'experience_years', 'overall_score')

    # تسمية الأعمدة بأسماء مفهومة (اختياري لكنه أفضل)
    column_labels = {
        'full_name': 'الاسم الكامل',
        'title': 'المسمى الوظيفي',
        'experience_years': 'سنوات الخبرة',
        'overall_score': 'مستوى التقدم %'
    }

    form_overrides = {
        'profile_image': FileUploadField
    }
    # def __init__(self, model, **kwargs):
    #     super().__init__(model, **kwargs)
    form_args = {
            'profile_image': {
                'label': 'Profile Image',
                'base_path': Config.UPLOAD_PATH,
                'relative_path': '',
                'allow_overwrite': True
            }
        }


class EducationView(ModelView):
    # الأعمدة التي تظهر في الجدول
    column_list = ('institution', 'degree', 'major', 'start_date', 'end_date')

    # البحث والفلترة
    column_searchable_list = ('institution', 'major')
    column_filters = ('degree',)

    # تسمية الحقول بالعربية
    column_labels = {
        'institution': 'المؤسسة التعليمية',
        'degree': 'الدرجة العلمية',
        'major': 'التخصص',
        'start_date': 'تاريخ البدء',
        'end_date': 'تاريخ التخرج'
    }

class CourseView(ModelView):
    # column_list = ('course_name', 'start_date', 'end_date')
    #
    # column_searchable_list = ('course_name', 'start_date', 'end_date')
    # column_filters = ('organization', 'start_date')

    column_formatters = {
        'acquired_skills': lambda v,c,m,p:', '.join(m.acquired_skills) if m.acquired_skills else "",
    }

    column_labels = {
        'course_name': 'اسم الكورس',
        'organization': 'المؤسسة/الشركة',
        'project_summary': 'نبذة عن المشروع التطبيقي',
        'start_date': 'تاريخ البدء',
        'end_date': 'تاريخ الانتهاء',
        'acquired_skills': 'المهارات المكتسبة',
        'last_updated': 'آخر تعديل'
    }

    def on_model_change(self, form, model, is_created):
        model.last_updated = datetime.now(timezone.utc)


class ProjectView(ModelView):
    column_list = ('project_name', 'github_url', 'last_updated')
    column_searchable_list = ('project_name', 'description')

    # column_filters = ('acquired_skills', 'last_updated')

    form_overrides = {
        'project_image': FileUploadField,
        'project_video': FileUploadField
    }

    form_args = {
        'project_image': {
            'label': 'Project Image',
            'base_path': Config.UPLOAD_PATH,
            'relative_path': '',
            'allow_overwrite': True
        },
        'project_video': {
            'label': 'Project Video',
            'base_path': Config.UPLOAD_PATH,
            'relative_path': '',
            'allow_overwrite': True
        }
    }
    column_labels = {
        'project_name': 'project_name',
        'github_url': 'github_url',
        'last_updated': 'last_updated',
        'project_video': 'project_video',
        'acquired_skills': 'acquired_skills',
        'description': 'description',
        'LAST_UPDATED': 'LAST_UPDATED'
    }

    def on_model_change(self, form, model, is_created):
        model.last_updated = datetime.now(timezone.utc)



class SelfStudyView(ModelView):
    column_list = ('title', 'platform_name', 'last_updated')

    column_searchable_list = ('title', 'platform_name')


    form_overrides = {
        'cover_image': FileUploadField,
        'sample_video': FileUploadField
    }

    form_args = {
        'cover_image': {
            'label': 'Cover Image',
            'base_path': Config.UPLOAD_PATH,
            'relative_path': '',
            'allow_overwrite': True
        },
        'sample_video': {
            'label': 'Sample Video',
            'base_path': Config.UPLOAD_PATH,
            'relative_path': '',
            'allow_overwrite': True
        }
    }

    column_labels = {
        'title': 'Title',
        'platform_name': 'Platform Name',
        'last_updated': 'Last Updated',
        'cover_image': 'Cover Image',
        'sample_video': 'Sample Video',
    }
    def on_model_change(self, form, model, is_current):
        model.last_updated = datetime.now(timezone.utc)

class ExperienceView(ModelView):
    column_list = ('job_title', 'company_name')
    column_searchable_list = ('job_title', 'company_name')

    column_filters = ('is_current', 'start_date')

    column_labels = {
        'job_title': 'Job Title',
        'company_name': 'Company Name',
        'start_date': 'Start Date',
        'end_date': 'End Date',
        'is_current': 'Is Created',
        'skills': 'Skills',
    }

    def on_model_change(self, form, model, is_current):
        model.last_updated = datetime.now(timezone.utc)
        if model.is_current:
            model.end_date = None


class AchievementView(ModelView):
    column_list = ('title', 'issuing_organization', 'date_obtained')
    # column_searchable_list = ('title', 'issuing_organization', 'date_obtained')
    # column_filters = ('date_obtained', 'skills_demonstrated')

    column_labels = {
        'title': 'Title',
        'issuing_organization': 'Issuing Organization',
        'date_obtained': 'Date Obtained',
        'skills_demonstrated': 'Skills Demonstrated',
        'description': 'Description',
        'last_updated': 'Last Updated',
    }

    def on_model_change(self, form, model, is_created):
        model.last_updated = datetime.now(timezone.utc)




