from mongoengine import Document, StringField, IntField, DateTimeField, ListField
from datetime import datetime,timezone


class Goal(Document):
    goal_name = StringField(required=True)
    required_skills = ListField(StringField())
    goal_score = IntField(default=0)
    last_updated = DateTimeField(default=datetime.now(timezone.utc))

    meta = {
        'collection': 'goals',
        'ordering': ['-last_updated']
    }

    def __str__(self):
        return f"{self.goal_name} ({self.goal_score}%)"