from mongoengine import Document, StringField, DateTimeField
from datetime import datetime, timezone


class Language(Document):
    language_name = StringField(required=True, unique=True)

    LEVEL_CHOICES = [
        ('A1', 'A1 - Beginner'),
        ('A2', 'A2 - Elementary'),
        ('B1', 'B1 - Intermediate'),
        ('B2', 'B2 - Upper Intermediate'),
        ('C1', 'C1 - Advanced'),
        ('C2', 'C2 - Proficient/Native'),
    ]

    level = StringField(required=True, choices=LEVEL_CHOICES)
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'languages',
        'ordering': ['-level']
    }

    def __str__(self):
        return f"{self.language_name} ({self.level})"
