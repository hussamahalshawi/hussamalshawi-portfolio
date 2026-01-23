from mongoengine import Document, StringField, DateTimeField, ListField
from datetime import datetime, timezone


class Achievement(Document):
    title = StringField(required=True)
    issuing_organization = StringField(required=True)
    date_obtained = DateTimeField(required=True)
    description = StringField()
    skills_demonstrated = ListField(StringField())
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'achievement',
        'ordering': ['-date_obtained']
    }

    def __str__(self):
        return f"{self.title} from {self.issuing_organization}"
