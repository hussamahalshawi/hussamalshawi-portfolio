from mongoengine import Document, StringField, DateTimeField
from datetime import datetime, timezone


class Category(Document):
    """
    A unified model for all types of classifications (Study Tracks, Project Categories, etc.).
    This keeps the code clean and centralizes category management.
    """
    name = StringField(required=True, unique=True)
    description = StringField()

    # حقل اختياري لتحديد نوع التصنيف إذا أردت فصلهم في لوحة التحكم لاحقاً
    # category_type = StringField(choices=('Study', 'Project', 'General'), default='General')

    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'categories',
        'ordering': ['name'],
        'indexes': ['name']
    }

    def __str__(self):
        return self.name