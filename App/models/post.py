from mongoengine import Document, StringField, ListField, URLField, DateTimeField, ReferenceField, IntField
from datetime import datetime, timezone


# --- TAXONOMY LAYER ---
class Series(Document):
    """
    Groups posts into logical series (e.g., 'رؤية مبرمج', 'خارج إطار الكود').
    Essential for organized storytelling and LinkedIn/Medium content strategy.
    """
    name = StringField(required=True, unique=True)

    # Audit trail for when the series was first established
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'series',
        'indexes': ['name']
    }

    def __str__(self):
        """Returns the series name for easy identification in Admin dropdowns."""
        return self.name


# --- CONTENT LAYER ---
class Post(Document):
    """
    Core blog/social media post model.
    Designed for 2026 SEO standards and high-performance content delivery.
    Tracks engagement metrics and handles multi-media assets.
    """

    # --- CORE CONTENT ---
    content = StringField()  # Supports long-form text (Markdown/HTML)

    # Relational link to the parent series
    series = ReferenceField(Series)

    # --- EXTERNAL SYNC ---
    # Stores the link to the original post on LinkedIn, Medium, or personal blog
    original_url = StringField()

    # --- ENGAGEMENT ANALYTICS ---
    # These fields can be updated via API integration or manual entry
    views_count = IntField()
    likes_count = IntField()
    shares_count = IntField()
    comments_count = IntField()

    # --- ASSETS & SEO ---
    post_images = ListField(StringField())  # List of image paths/URLs
    post_videos = StringField()  # Main video asset URL
    post_tags = ListField(StringField())  # Keywords for AI-Search optimization

    # --- TIMESTAMPS ---
    # Using lambda for real-time timestamp generation on document creation
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'posts',
        'strict': False,
        'ordering': ['-created_at'],  # Prioritize latest content
        'indexes': [
            'series',
            '-created_at',  # Optimized for chronological feed generation
            'post_tags'  # Optimized for keyword/category filtering
        ]
    }
