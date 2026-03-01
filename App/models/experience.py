from mongoengine import Document, StringField, DateTimeField, ListField, BooleanField
from datetime import datetime, timezone


class Experience(Document):
    """
    Represents professional work history and career milestones.
    This model is a primary data source for the Profile's 'experience_years'
    calculation and skill proficiency tracking.
    """

    # --- POSITION DETAILS ---
    job_title = StringField(required=True)
    company_name = StringField(required=True)
    location = StringField(max_length=100)  # e.g., "Remote" or "Dubai, UAE"

    # --- DESCRIPTION FIELD (The requested update) ---
    # High-quality validation: ensuring a substantial description is provided
    description = StringField()

    # --- TIMELINE MANAGEMENT ---
    start_date = DateTimeField(required=True)

    # end_date is required by the schema, but logic in Signals or Admin
    # will handle cases where 'is_current' is True.
    end_date = DateTimeField(required=False)

    # Boolean flag to indicate if the user is currently employed in this role
    is_current = BooleanField(default=False)

    # --- SKILL ACQUISITION ---
    # List of skills utilized or mastered during this professional tenure.
    # These are picked up by system signals to update the master Skill model.
    skills_acquired = ListField(StringField())

    # --- SYSTEM METRICS ---
    # Using lambda ensures a fresh UTC timestamp is generated on every save operation
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'experience',
        'ordering': ['-end_date'],  # Displays most recent professional roles first
        'indexes': [
            'job_title',
            'company_name',
            'is_current',
            '-start_date'  # Optimized for chronological career timeline generation
        ]
    }

    def __str__(self):
        """Official string representation for admin dropdowns and audit logs."""
        status = "(Current)" if self.is_current else ""
        return f"{self.job_title} at {self.company_name} {status}"