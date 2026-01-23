from mongoengine import Document, StringField, ListField, URLField, DateTimeField, ReferenceField, IntField
from datetime import datetime, timezone



class Series(Document):
    name = StringField(required=True, unique=True)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    def __str__(self):
        return self.name

class Post(Document):
    title = StringField(required=True)
    content = StringField()
    series = ReferenceField(Series, required=True)
    original_url = URLField()
    views_count = IntField()
    likes_count = IntField()
    shares_count = IntField()
    comments_count = IntField()

    post_images = ListField(StringField())
    post_videos = StringField()
    post_tags = ListField(StringField())
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))


    meta = {
        'collection': 'posts',
        'ordering': ['-created_at']
    }

    def __str__(self):
        return self.title