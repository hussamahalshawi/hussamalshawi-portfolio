from mongoengine import Document, StringField, FloatField, DateTimeField, EmailField
from datetime import datetime, timezone


class Profile(Document):
    """
    The Central Hub of the portfolio.
    Manages personal identity and orchestrates global score calculations.
    """

    # --- IDENTITY & CONTACT ---
    full_name = StringField(required=True, default="Hussam Alshawi")
    title = StringField(required=True)
    bio = StringField(required=True)
    email = EmailField(required=True, unique=True)
    phone = StringField()
    address = StringField(help_text="City, Country")

    # --- SOCIAL ECOSYSTEM ---
    github_url = StringField()
    linkedin_url = StringField()
    facebook_url = StringField()
    instagram_url = StringField()

    # --- ASSETS & METRICS ---
    profile_image = StringField()
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))

    # PERSISTED METRICS: These are recalculated via signals
    experience_years = FloatField(default=0.0)
    overall_score = FloatField(default=0.0)

    meta = {
        'collection': 'profile',
        'indexes': ['email']  # Optimized for fast identity retrieval
    }

    # --- LOGIC: REFRESH ALL METRICS ---
    def refresh_metrics(self):
        """
        Global trigger to recalculate everything.
        Ensures deleted items are removed from the total count.
        """
        self.experience_years = self.calculate_total_experience()
        self.overall_score = self.calculate_overall_score()
        self.save()

    def calculate_total_experience(self):
        """
        Calculates total years of experience by aggregating durations from
        different activities, multiplied by their respective importance weights.
        """
        from App.models.experience import Experience
        from App.models.course import Course
        from App.models.education import Education
        from App.models.project import Project
        from App.models.self_study import SelfStudy
        from datetime import datetime, timezone

        total_weighted_days = 0
        now = datetime.now(timezone.utc)

        # Defined weights for each contribution type
        weights = {
            'Experience': 1.0,  # Full weight for professional jobs
            'Project': 0.4,  # Projects count as 40% of standard time
            'Education': 0.2,  # Degree time counts as 20%
            'SelfStudy': 0.3,  # Independent study counts as 30%
            'Course': 0.3  # Certified courses count as 30%
        }

        model_list = [Experience, Project, Education, SelfStudy, Course]

        for model in model_list:
            weight = weights.get(model.__name__, 0.1)

            for item in model.objects.all():
                # Check if start_date exists and is valid
                if hasattr(item, 'start_date') and item.start_date:
                    # Ensure start_date is timezone-aware
                    start = item.start_date.replace(
                        tzinfo=timezone.utc) if not item.start_date.tzinfo else item.start_date

                    # Use end_date if available and not null, otherwise assume it's an ongoing activity (today)
                    if hasattr(item, 'end_date') and item.end_date:
                        end = item.end_date.replace(tzinfo=timezone.utc) if not item.end_date.tzinfo else item.end_date
                    else:
                        end = now

                    # Calculate duration in days and apply the specific weight
                    duration_days = (end - start).days
                    if duration_days > 0:
                        total_weighted_days += duration_days * weight

        # Convert total days into years using the standard orbital year (365.25 days)
        return round(total_weighted_days / 365.25, 1)

    def calculate_overall_score(self):
        """
        Calculates the general progress percentage by averaging the
        completion rates of all existing goals.
        """
        from App.models.goal import Goal

        goals = Goal.objects.all()
        if not goals:
            return 0.0

        total_progress_percentage = 0.0

        for goal in goals:
            # Avoid division by zero if target_score is not set or set to 0
            target = goal.target_score if goal.target_score and goal.target_score > 0 else 100

            # Calculate individual goal progress
            progress = (goal.current_score / target) * 100
            # Ensure individual progress doesn't exceed 100%
            total_progress_percentage += min(progress, 100)

        # Calculate the mean (average) across all goals
        overall_average = total_progress_percentage / len(goals)

        return round(overall_average, 1)
    def __str__(self):
        return self.full_name