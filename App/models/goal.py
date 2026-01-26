from mongoengine import Document, StringField, IntField, DateTimeField, ListField
from datetime import datetime,timezone


class Goal(Document):
    goal_name = StringField(required=True, unique=True)
    description = StringField()
    target_score = IntField(default=95)
    current_score = IntField(default=0)
    required_skills = ListField(StringField())
    last_updated = DateTimeField(default=datetime.now(timezone.utc))

    meta = {
        'collection': 'goals',
        'ordering': ['-last_updated']
    }

    def sync_with_existing_skills(self):
        """
        Updates the goal's current score based on the proficiency levels
        of related skills in the database.
        """
        from App.models.skill import Skill

        # 1. Normalize skill names to Title Case (e.g., 'python' -> 'Python')
        if self.required_skills:
            self.required_skills = [str(s).strip().capitalize() for s in self.required_skills]
        else:
            # Return 0 if no skills are assigned to this goal
            return 0

        total_xp = 0.0

        # 2. Iterate through required skills to calculate aggregate score
        for skill_req in self.required_skills:
            # Perform a case-insensitive search for the skill
            skill_obj = Skill.objects(skill_name__iexact=skill_req).first()

            if skill_obj:
                # Calculation Logic: Each skill contributes a weighted percentage
                # Example: A skill at level 80 contributes (80/100) * 25 = 20 points
                contribution = (skill_obj.level / 100) * 25
                total_xp += contribution

        # 3. Cap the final score to target_score or a default maximum of 95
        max_attainable = self.target_score if self.target_score else 95
        self.current_score = min(total_xp, max_attainable)

        return self.current_score

    def __str__(self):
        return f"{self.goal_name} ({self.current_score}%)"