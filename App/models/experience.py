from mongoengine import Document, StringField, DateTimeField, ListField, BooleanField
from datetime import datetime, timezone



class Experience(Document):
    job_title = StringField(required=True, max_length=200)
    company_name = StringField(required=True, max_length=200)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField()
    is_current = BooleanField(default=False)
    skills_acquired = ListField(StringField())
    last_updated = DateTimeField(default=datetime.now(timezone.utc))

    meta = {
        'collection': 'experience',
        'ordering': ['-start_date']
    }

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"