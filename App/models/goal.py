from mongoengine import Document, StringField, IntField, DateTimeField, ListField
from datetime import datetime,timezone


class Goal(Document):
    goal_name = StringField(required=True)
    description = StringField()
    target_score = IntField(default=100)
    current_score = IntField(default=0)
    required_skills = ListField(StringField())
    last_updated = DateTimeField(default=datetime.now(timezone.utc))

    meta = {
        'collection': 'goals',
        'ordering': ['-last_updated']
    }

    def __str__(self):
        return f"{self.goal_name} ({self.current_score}%)"