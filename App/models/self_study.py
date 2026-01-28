from mongoengine import Document, StringField, DateTimeField, ListField
from datetime import datetime, timezone


class SelfStudy(Document):
    """
    Represents independent learning activities, online courses, or certifications.
    This model tracks personal growth and contributes to skill level calculations.
    """

    # --- CORE INFORMATION ---
    title = StringField(required=True)
    platform_name = StringField(required=True)  # e.g., Coursera, Udemy, YouTube
    summary = StringField()  # Brief overview of what was studied

    # --- MEDIA ASSETS ---
    # Stores paths or URLs for the study materials
    cover_image = StringField()
    sample_video = StringField()

    # --- TIMELINE ---
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)

    # --- SKILLS ACQUISITION ---
    # List of skills to be processed by the master sync signal
    skills_learned = ListField(StringField())

    # --- AUDIT METRICS ---
    # Using lambda to ensure a fresh timestamp is generated at the moment of creation
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'self_study',
        'ordering': ['-created_at'],
        'indexes': [
            'title',
            'platform_name',
            '-created_at'  # Optimized for high-speed chronological queries
        ]
    }

    def __str__(self):
        """String representation for the admin interface and debugging."""
        return f"{self.title} via {self.platform_name}"