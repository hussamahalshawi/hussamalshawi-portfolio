from mongoengine import Document, StringField, DateTimeField, ListField
from datetime import datetime, timezone


class Achievement(Document):
    """
    Represents professional awards, recognitions, and major career milestones.
    This model highlights exceptional performance and validation of high-level skills.
    """

    # --- RECOGNITION DETAILS ---
    title = StringField(required=True)  # e.g., Employee of the Month, Hackathon Winner
    issuing_organization = StringField()  # The entity that granted the recognition

    # --- DATE & DESCRIPTION ---
    date_obtained = DateTimeField(required=True)
    description = StringField()  # Detailed context of why this achievement was granted

    # --- SKILL VALIDATION ---
    # Specific skills that were proven or utilized to earn this achievement
    skills_demonstrated = ListField(StringField())

    # --- AUDIT METRICS ---
    # Ensures the record tracks the last synchronization or manual edit time
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'achievements',  # Pluralized for standard naming conventions
        'ordering': ['-date_obtained'],  # Displays most recent achievements at the top
        'indexes': [
            'title',
            'issuing_organization',
            '-date_obtained'  # Optimized for chronological sorting in the UI
        ]
    }

    def __str__(self):
        """Official string representation for admin logs and displays."""
        org = f" from {self.issuing_organization}" if self.issuing_organization else ""
        return f"{self.title}{org}"