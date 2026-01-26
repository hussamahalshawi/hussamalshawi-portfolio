from mongoengine import Document, StringField, DateTimeField, ListField, BooleanField
from datetime import datetime, timezone



class Experience(Document):
    job_title = StringField(required=True)
    company_name = StringField(required=True)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    is_current = BooleanField(default=False)
    skills_acquired = ListField(StringField())
    last_updated = DateTimeField(default=datetime.now(timezone.utc))

    meta = {
        'collection': 'experience',
        'ordering': ['-start_date']
    }

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"