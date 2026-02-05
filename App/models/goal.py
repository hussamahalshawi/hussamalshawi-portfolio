from mongoengine import Document, StringField, IntField, DateTimeField, ListField
from datetime import datetime,timezone


class Goal(Document):
    """
    Career Roadmap Goal model.
    Tracks proficiency targets based on specific skill sets for each milestone.
    """

    # --- CORE FIELDS ---
    goal_name = StringField(required=True, unique=True)
    sub_title = StringField()
    target_year = IntField(required=True)

    # --- METRICS ---
    target_score = IntField(default=95)
    current_score = IntField(default=0)

    # --- RELATIONSHIPS ---
    required_skills = ListField(StringField())

    # --- METADATA ---
    # Fix: Use lambda to ensure the current time is evaluated during each save,
    # not just once when the application starts.
    last_updated = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'goals',
        'ordering': ['-last_updated'],
        'indexes': [
            'goal_name',
            'target_year'
        ]
    }
    def sync_with_existing_skills(self):
        """
        Calculates the goal's current score based on the weighted contribution of required skills.
        Logic:
        - 1 Skill: Each point of skill level accounts for 100% of the goal's weight.
        - 3 Skills: Each skill accounts for 33.3% of the total goal weight.
        Formula: (Current_Skill_Level / 100) * (100 / Total_Required_Skills)
        """
        from App.models.skill import Skill

        # 1. Data validation: Return 0 if no skills are associated with this goal
        if not self.required_skills:
            self.current_score = 0
            return 0

        # Normalize skill names for consistent database lookups
        self.required_skills = [str(s).strip().capitalize() for s in self.required_skills]

        # 2. Calculate the relative weight for each skill (Equal distribution of 100%)
        total_skills_count = len(self.required_skills)
        weight_per_skill = 100.0 / total_skills_count

        total_weighted_score = 0.0

        # 3. Aggregate weighted contributions from each existing skill
        for skill_req in self.required_skills:
            # Case-insensitive query to find the skill in the database
            skill_obj = Skill.objects(skill_name__iexact=skill_req).first()

            if skill_obj:
                # Skill contribution = (Proficiency percentage) * (Assigned weight in this goal)
                # Example: A skill at 80% level in a 2-skill goal contributes (0.8 * 50) = 40 points
                contribution = (skill_obj.level / 100.0) * weight_per_skill
                total_weighted_score += contribution
            else:
                # Non-existent skills contribute 0 points to the progress
                total_weighted_score += 0

        # 4. Finalize the score within the bounds of target_score or system default (95)
        max_attainable = self.target_score if self.target_score else 95

        # Rounding to the nearest integer for clean UI representation
        self.current_score = min(round(total_weighted_score), max_attainable)

        return self.current_score

    def __str__(self):
        return f"{self.goal_name} ({self.current_score}%)"