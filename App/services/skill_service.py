from App.models.skill import Skill, SkillType
from datetime import datetime, timezone
import logging


class SkillService:
    """
    Advanced Categorization Service for HussamAlshawi-Portfolio.
    Implements Token-based matching to resolve "Communication Skills"
    and "Labor Law" misclassification issues.
    """

    @staticmethod
    def bulk_update_categories():
        """
        Updates skill categories based on exact word matches (Tokens).
        Zero-Score logic ensures non-matching skills don't default to the first group.
        """
        updated_count = 0

        try:
            all_skills = Skill.objects.all()
            all_types = SkillType.objects.all()

            # Safeguard against empty SkillTypes
            if not all_types:
                logging.error("Categorization aborted: No SkillTypes found in database.")
                return 0

            # Pre-fetch 'Other technologies' to use as a safe fallback if desired
            other_tech_type = SkillType.objects(name__iexact="Other technologies").first()

            for skill in all_skills:
                # 1. Normalize and Tokenize the skill name
                skill_tokens = set(skill.skill_name.lower().strip().split())

                best_matched_type = None
                highest_match_score = 0

                for s_type in all_types:
                    if not s_type.keywords:
                        continue

                    # 2. Double Tokenization: Split multi-word keywords into individual tokens
                    type_tokens = set()
                    for keyword in s_type.keywords:
                        type_tokens.update(keyword.lower().strip().split())

                    # 3. Intersection Logic: Match whole words only
                    common_words = skill_tokens.intersection(type_tokens)
                    match_score = len(common_words)

                    # 4. Rank by Match Score
                    if match_score > highest_match_score:
                        highest_match_score = match_score
                        best_matched_type = s_type

                # 5. Final Assignment Logic (Zero-Score Protection)
                final_type = None

                if highest_match_score > 0:
                    # High confidence match found
                    final_type = best_matched_type
                elif other_tech_type:
                    # No match found - Defaulting to "Other technologies"
                    final_type = other_tech_type

                # 6. Database Update Validation
                if final_type and skill.skill_type != final_type:
                    skill.skill_type = final_type
                    skill.last_updated = datetime.now(timezone.utc)
                    skill.save()
                    updated_count += 1

        except Exception as e:
            logging.error(f"Critical error in SkillService: {str(e)}")
            raise Exception(f"Professional Categorization failed: {str(e)}")

        return updated_count