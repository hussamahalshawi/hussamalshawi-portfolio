from mongoengine import Document, StringField, DateTimeField, EmailField
from datetime import datetime, timezone


class Feedback(Document):
    """
    Captures professional testimonials and recommendations from clients or colleagues.
    This model serves as 'Social Proof' to validate technical reliability and soft skills.
    """

    # --- CONTRIBUTOR IDENTITY ---
    person_name = StringField(required=True)
    job_title = StringField()  # e.g., Senior Developer, Project Manager

    # --- CONTENT & MESSAGE ---
    # Stores the testimonial text provided by the individual
    feedback_text = StringField()

    # --- COMMUNICATION CHANNELS ---
    # Required for verification or following up with the feedback provider
    contact_email = EmailField(required=True)

    # Optional field for LinkedIn profile URL or Phone Number
    contact_info = StringField(required=False)

    # --- AUDIT & TIMELINES ---
    # Automatically captures the exact moment the feedback was submitted
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'feedback',
        'ordering': ['-created_at'],  # Displays latest testimonials first
        'indexes': [
            'person_name',
            'contact_email',
            '-created_at'  # Optimized for dashboard and public view performance
        ]
    }

    def __str__(self):
        """Standardized string representation for admin logs and display."""
        return f"Feedback from: {self.person_name}"