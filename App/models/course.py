from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField
from datetime import datetime, timezone


class Course(Document):
    course_name = StringField(required=True)
    organization = StringField()

    project_summary = StringField()
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    acquired_skills = ListField(StringField())
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))


    meta = {
        'collection': 'courses',
        'ordering': ['-start_date']
    }


    def __str__(self):
        return self.course_name