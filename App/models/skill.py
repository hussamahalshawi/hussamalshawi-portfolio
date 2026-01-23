from mongoengine import Document, StringField, DateTimeField, IntField, ReferenceField, ListField
from datetime import datetime, timezone

class SkillType(Document):
    name = StringField(required=True, unique=True)
    keywords = ListField(StringField())

    meta = {
        'collection': 'skill_types'
    }

    def __str__(self):
        return self.name


class Skill(Document):
    skill_name = StringField(required=True, unique=True)
    skill_type = ReferenceField(SkillType)
    level = IntField()
    last_updated = DateTimeField(default=datetime.now(timezone.utc))

    meta = {
        'collection': 'skills',
        'ordering': ['-level']
    }

    def __str__(self):
        return f"{self.skill_name} - {self.level}%"

