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
        Advanced Skill Mapping Logic:
        1. Splits goal skill strings into individual words (Tokens).
        2. Compares each word with official skills (also tokenized).
        3. If multiple matches occur, it calculates the mean (Average) of those skills.
        4. Calculates the final weighted score for the goal.
        """
        from App.models.skill import Skill
        import numpy as np  # Optional, but we'll use standard math for simplicity

        if not self.required_skills:
            self.current_score = 0
            return 0

        total_weighted_score = 0.0
        total_skills_to_track = len(self.required_skills)
        weight_per_entry = 100.0 / total_skills_to_track

        # --- THE CORE LOGIC: Tokenization and Matching ---
        for goal_skill_str in self.required_skills:
            # Step A: Split the goal skill into words (e.g., "Python Backend" -> ["python", "backend"])
            goal_tokens = set(goal_skill_str.lower().strip().split())

            matched_skills_levels = []

            # Step B: Iterate through ALL official skills to find partial matches
            all_official_skills = Skill.objects.all()
            for official_skill in all_official_skills:
                # Tokenize official skill name (e.g., "Python Language" -> ["python", "language"])
                official_tokens = set(official_skill.skill_name.lower().strip().split())

                # Step C: Intersection Check (Are there common words?)
                if goal_tokens.intersection(official_tokens):
                    matched_skills_levels.append(official_skill.level)

            # Step D: Handle the result for this specific entry
            if matched_skills_levels:
                # If multiple skills match, take the Mean (Average) as requested
                average_level = sum(matched_skills_levels) / len(matched_skills_levels)

                # Calculate contribution: (Average Level / 100) * (Weight)
                contribution = (average_level / 100.0) * weight_per_entry
                total_weighted_score += contribution
            else:
                # No match found for this entry
                total_weighted_score += 0

        # Finalize Goal Score
        max_attainable = self.target_score if self.target_score else 95
        self.current_score = min(round(total_weighted_score), max_attainable)
        self.last_updated = datetime.now(timezone.utc)

        return self.current_score
    def __str__(self):
        return f"{self.goal_name} ({self.current_score}%)"