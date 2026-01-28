from mongoengine import Document, StringField, DateTimeField, IntField, ReferenceField, ListField
from datetime import datetime, timezone


# --- CLASSIFICATION LAYER ---
class SkillType(Document):
    """
    Represents the categorization of skills (e.g., Frontend, Backend, Soft Skills).
    Used to group individual skills for better UI/UX filtering.
    """
    name = StringField(required=True, unique=True)
    keywords = ListField(StringField())  # Tags used for AI-based skill matching

    meta = {
        'collection': 'skill_types',
        'indexes': ['name']  # Performance optimization for searching categories
    }

    def __str__(self):
        return self.name


# --- CORE DATA LAYER ---
class Skill(Document):
    """
    Core model representing a professional skill and its proficiency level.
    Levels are automatically synchronized via system signals.
    """
    skill_name = StringField(required=True, unique=True)
    skill_type = ReferenceField(SkillType)

    # Proficiency percentage (0-100), updated based on projects/courses
    level = IntField(default=0)

    # Audit timestamp for tracking synchronization events
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'skills',
        'ordering': ['-level'],  # Display strongest skills first by default
        'indexes': ['skill_name', 'level']  # Indexed for high-speed score retrieval
    }

    def __str__(self):
        """Returns a readable representation of the skill and its strength."""
        return f"{self.skill_name} - {self.level}%"