from mongoengine import Document, StringField, DateTimeField, ListField
from datetime import datetime, timezone


class SelfStudy(Document):
    title = StringField(required=True)
    platform_name = StringField(required=True)

    summary = StringField()
    cover_image = StringField()
    sample_video = StringField()
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    skills_learned = ListField(StringField())

    created_at = DateTimeField(default=datetime.now(timezone.utc))
    last_updated = DateTimeField(default=datetime.now(timezone.utc))


    meta = {
        'collection': 'self_study',
        'ordering': ['-created_at']
    }


    def __str__(self):
        return self.title