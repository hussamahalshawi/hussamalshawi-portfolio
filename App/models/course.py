from mongoengine import Document, StringField, DateTimeField, ListField
from datetime import datetime, timezone


class Course(Document):
    """
    Represents professional certifications and training courses.
    Plays a key role in skill leveling (30% weight) and serves as
    evidence of continuous professional development.
    """

    # --- COURSE IDENTIFICATION ---
    course_name = StringField(required=True)
    organization = StringField()  # e.g., IBM, Google, Meta, or local institutes

    # --- PROJECT-BASED LEARNING ---
    # Briefly describes the practical project completed during the course
    project_summary = StringField()

    # --- TIMELINE ---
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)

    # --- SKILLS ENGINE ---
    # Skills tagged here will be synchronized with the master Skill model
    acquired_skills = ListField(StringField())

    # --- AUDIT & SYNC ---
    # Using lambda to ensure a unique UTC timestamp is generated on every save
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'courses',
        'ordering': ['-start_date'],  # Displays newest courses first
        'indexes': [
            'course_name',
            'organization',
            '-start_date'  # Optimized for high-speed chronological listing
        ]
    }

    def __str__(self):
        """Official identifier for the course in admin views and logs."""
        return f"{self.course_name} by {self.organization}" if self.organization else self.course_name