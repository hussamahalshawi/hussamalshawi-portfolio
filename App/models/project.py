from mongoengine import Document, StringField, ListField, URLField, DateTimeField
from datetime import datetime, timezone


class Project(Document):
    project_name = StringField(required=True, unique=True)
    description = StringField(required=True)
    github_url = URLField(required=True)

    project_image = StringField()
    project_video = StringField()

    skills_used = ListField(StringField())
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))


    meta = {
        'collection': 'projects',
        'ordering': ['-last_updated']
    }

    def __str__(self):
        return self.project_name