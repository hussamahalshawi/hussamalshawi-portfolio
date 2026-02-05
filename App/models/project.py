from mongoengine import Document, StringField, ListField, URLField, DateTimeField, ReferenceField
from datetime import datetime, timezone
from App.models.category import Category


class Project(Document):
    """
    Core model for showcasing technical projects.
    Integrates with the skill-sync system to reflect technical proficiency
    based on the 'skills_used' field.
    """

    # --- IDENTIFICATION & LINKS ---
    project_name = StringField(required=True, unique=True)
    description = StringField(required=True)

    # URLField provides built-in validation for correct link formatting
    github_url = URLField(null=True, blank=True)

    # --- CATEGORIZATION (DYNAMIC LINK) ---
    # Links each project to a category managed via the admin panel
    category = ReferenceField(Category)

    # --- MEDIA ASSETS ---
    # Stores relative paths to images and videos for visual presentation
    project_image = StringField()
    project_video = StringField()

    # --- PROJECT TIMELINE ---
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)

    # --- TECH STACK & AUTOMATION ---
    # This list is tracked by 'master_sync_signal' to update Skill levels
    skills_used = ListField(StringField())

    # --- AUDIT METRICS ---
    # Using lambda to ensure the timestamp is generated at the exact moment of saving
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'projects',
        'ordering': ['-last_updated'],  # Displays most recently updated projects first
        'indexes': [
            'project_name',
            '-last_updated'  # Optimized for high-speed chronological sorting
        ]
    }

    def __str__(self):
        """Official string representation for admin logs and dropdowns."""
        return self.project_name