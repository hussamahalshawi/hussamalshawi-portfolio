from mongoengine import Document, StringField, URLField, DateTimeField, DictField, EmailField, IntField
from datetime import datetime, timezone, tzinfo


class Profile(Document):
    full_name = StringField(required=True, default="Hussam Alshawi")
    title = StringField(required=True)
    bio = StringField(required=True)
    email = EmailField(required=True, unique=True)
    phone = StringField()
    address = StringField(help_text="المدينة، الدولة")
    # social_links = DictField(help_text="أدخل المفتاح كاسم المنصة والرابط كقيمة. مثال: {'github': 'url'}")
    github_url = StringField()
    linkedin_url = StringField()
    facebook_url = StringField()
    instagram_url = StringField()
    profile_image = StringField()
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))
    career_start_date = DateTimeField(required=True, help_text="start date of career")

    overall_score = IntField(default=0, min_value=0, max_value=100)


    meta = {
        'collection': 'profile'
    }

    @property
    def experience_years(self):
        if not self.career_start_date:
            return 0
        today = datetime.now(timezone.utc)
        start_date = self.career_start_date.replace(tzinfo=timezone.utc) if self.career_start_date.tzinfo is None else self.career_start_date

        diff = today - start_date
        years = diff.days / 365.25
        return round(years, 1)

    def __str__(self):
        return self.full_name