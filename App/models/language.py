from mongoengine import Document, StringField, DateTimeField
from datetime import datetime, timezone


class Language(Document):
    """
    Represents language proficiency levels following the CEFR standard.
    This model showcases communication capabilities for international job applications.
    """

    # --- CORE DATA ---
    language_name = StringField(required=True, unique=True)  # e.g., English, Arabic, German

    # --- CEFR STANDARDS ---
    # Common European Framework of Reference for Languages
    LEVEL_CHOICES = [
        ('A1', 'A1 - Beginner'),
        ('A2', 'A2 - Elementary'),
        ('B1', 'B1 - Intermediate'),
        ('B2', 'B2 - Upper Intermediate'),
        ('C1', 'C1 - Advanced'),
        ('C2', 'C2 - Proficient/Native'),
    ]

    # Level selection based on standard choices to ensure data consistency
    level = StringField(required=True, choices=LEVEL_CHOICES)

    # --- AUDIT METRICS ---
    # Ensures the last update timestamp is generated dynamically at the time of save
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'languages',
        'ordering': ['-level'],  # Sort by highest proficiency first
        'indexes': [
            'language_name',
            'level'
        ]
    }

    def __str__(self):
        """Official string representation for admin UI and profile display."""
        return f"{self.language_name} ({self.level})"