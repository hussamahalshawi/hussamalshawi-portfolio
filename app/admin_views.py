import os
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
