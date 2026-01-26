from mongoengine import Document, StringField,DateTimeField, EmailField, URLField
from datetime import datetime, timezone


class Feedback(Document):
    person_name = StringField(required=True)
    job_title = StringField()
    feedback_text = StringField()
    contact_email = EmailField(required=True)
    contact_info = StringField(required=False)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'feedback',
        'ordering': ['-created_at']
    }

    def __str__(self):
        return f"Feedback: {self.person_name}"