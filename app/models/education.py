from mongoengine import (
Document,
StringField,
DateTimeField,
FloatField,
ListField
)
from datetime import datetime

class Education(Document):
    institution = StringField(required=True)
    degree = StringField(required=True)
    major = StringField(required=True)
    start_date = StringField(required=True)
    end_date = StringField()
    grade = StringField()
    description = StringField()
    related_skills = ListField(StringField())

    meta = {
        'collection': 'education',
        'ordering': ['-start_date']
    }


    def __str__(self):
        return f'{self.institution} {self.degree} {self.major}'