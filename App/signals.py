from mongoengine import signals
from App.models.goal import Goal
from App.models.project import Project
from App.models.course import Course
from App.models.experience import Experience
from App.models.education import Education
from App.models.self_study import SelfStudy
from App.models.achievement import Achievement
from App.models.skill import Skill, SkillType


def clean_and_normalize_input(value):
    """
    Cleans the input string by removing leading/trailing whitespaces
    and converting it to uppercase for consistent database lookups.
    """
    # 1. Check if value is None or purely consists of whitespace
    if value is None or not str(value).strip():
        return None

    # 2. Convert to string, remove extra spaces, and transform to uppercase
    # This ensures 'python', 'Python ', and 'PYTHON' are treated identically
    normalized_value = str(value).strip().upper()

    return normalized_value


def get_skill_metadata(skill_name_raw):
    """
    Advanced Skill Categorization using Tokenization logic.
    Ensures that newly added skills are categorized based on word-match scores.
    """
    if not skill_name_raw:
        return None, None

    # 1. Normalize and Tokenize the input skill
    skill_tokens = set(str(skill_name_raw).lower().strip().split())

    all_types = SkillType.objects.all()
    best_matched_type = None
    highest_match_score = 0
    official_name = str(skill_name_raw).strip().capitalize()

    # 2. Advanced Token Matching Logic
    for s_type in all_types:
        if not s_type.keywords:
            continue

        # Double Tokenization: Split all keywords in the category into words
        type_tokens = set()
        for keyword in s_type.keywords:
            type_tokens.update(str(keyword).lower().strip().split())

        # Intersection check (Exact word matching)
        common_words = skill_tokens.intersection(type_tokens)
        match_score = len(common_words)

        if match_score > highest_match_score:
            highest_match_score = match_score
            best_matched_type = s_type

    # 3. Final Assignment Logic
    if highest_match_score > 0:
        # If we found a match, we can also try to find the 'canonical' name from the keywords
        # For simplicity, we keep the user's input capitalized as the official name
        return best_matched_type, official_name

    # Fallback to "Other technologies" if score is 0
    other_tech_type = SkillType.objects(name__iexact="Other technologies").first()
    return other_tech_type, official_name


def recalculate_skill_total(official_name, s_type):
    """
    Scans all related models to aggregate a skill's total level based on
    historical data and predefined weights.
    """
    if not official_name:
        return

    # 1. Define models, their specific fields, and their contribution weights
    search_config = [
        (Project, 'skills_used', 10),
        (Course, 'acquired_skills', 15),
        (Experience, 'skills_acquired', 20),
        (Education, 'skills_learned', 5),
        (SelfStudy, 'skills_learned', 8),
        (Achievement, 'skills_demonstrated', 30)
    ]

    total_score = 0
    name_to_search = str(official_name).strip()

    # 2. Iterate through models and calculate total weighted score
    for model, field, weight in search_config:
        # Use iexact to ensure all case variations are counted
        occurrence_count = model.objects(**{f"{field}__iexact": name_to_search}).count()
        total_score += (occurrence_count * weight)

    # 3. Synchronize with the Skill collection
    if total_score > 0:
        # Using update_one with upsert=True to prevent NotUniqueError and ensure consistency
        Skill.objects(skill_name__iexact=name_to_search).update_one(
            set__skill_name=name_to_search,
            set__skill_type=s_type,
            set__level=min(total_score, 95), # Cap skill level at 95%
            upsert=True
        )
    else:
        # Remove the skill if it no longer exists in any activity
        Skill.objects(skill_name__iexact=name_to_search).delete()

# --- 3. إدارة مستويات المهارات ---
def handle_skill_level(sender, document, **kwargs):
    """
    Acts as a dispatcher that identifies skill fields from different models
    and triggers a full recalculation for each detected skill.
    """
    # 1. Prevent infinite recursion by ignoring Skill and Goal models
    if sender in [Goal, Skill]:
        return

    # 2. Configuration mapping for models and their respective skill fields
    model_field_map = {
        'Project': 'skills_used',
        'Course': 'acquired_skills',
        'Experience': 'skills_acquired',
        'Education': 'skills_learned',
        'SelfStudy': 'skills_learned',
        'Achievement': 'skills_demonstrated'
    }

    model_name = sender.__name__
    if model_name not in model_field_map:
        return

    # 3. Retrieve skills from the document and remove duplicates in the same entry
    target_field = model_field_map[model_name]
    raw_skills = getattr(document, target_field, []) or []

    # Use set() to avoid recalculating the same skill multiple times for one document
    unique_skills = list(set(raw_skills))

    for s_name in unique_skills:
        # Clean and normalize the skill name (e.g., ' python ' -> 'PYTHON')
        clean_name_upper = clean_and_normalize_input(s_name)
        if not clean_name_upper:
            continue

        # Fetch official metadata and canonical name
        s_type, official_name = get_skill_metadata(clean_name_upper)

        # Determine the final display name: Use official name or capitalize the input
        final_name = official_name if official_name else str(s_name).strip().capitalize()

        # Trigger the comprehensive recalculation engine
        recalculate_skill_total(final_name, s_type)


def master_sync_signal(sender, document, **kwargs):
    """
    The central coordinator that synchronizes skills, goals, and profile metrics
    whenever a change occurs in the tracked models.
    """
    from App.models.profile import Profile
    from App.models.goal import Goal

    # 1. Goal Personalization: Ensure required skills are formatted correctly
    if isinstance(document, Goal) and document.required_skills:
        # Format skills to Title Case for UI consistency
        formatted_skills = [str(s).strip().capitalize() for s in document.required_skills]

        # Direct database update to avoid triggering the signal recursively
        Goal.objects(id=document.id).update_one(set__required_skills=formatted_skills)
        document.required_skills = formatted_skills

    # 2. Skill Level Processing: Recalculate levels for all affected skills
    handle_skill_level(sender, document)

    # 3. Goals Synchronization: Update the progress score for all goals
    all_goals = Goal.objects.all()
    for goal in all_goals:
        # Calculate new progress based on updated skill levels
        updated_score = goal.sync_with_existing_skills()
        Goal.objects(id=goal.id).update_one(set__current_score=updated_score)

    # 4. Profile Finalization: Update global experience and overall achievement score
    user_profile = Profile.objects.first()
    if user_profile:
        new_experience = user_profile.calculate_total_experience()
        new_total_score = user_profile.calculate_overall_score()

        # Final persistence of profile metrics
        Profile.objects(id=user_profile.id).update_one(
            set__experience_years=new_experience,
            set__overall_score=new_total_score
        )

        # Logging for development tracking
        model_name = sender.__name__.upper()
        print(f"🚀 Master Sync [SUCCESS]: {model_name} synced | Exp: {new_experience}Y | Score: {new_total_score}%")


def master_delete_signal(sender, document, **kwargs):
    """
    Handles the cleanup process after a document is deleted.
    It recalculates skills, goals, and profile metrics to ensure data integrity.
    """
    from App.models.profile import Profile
    from App.models.goal import Goal

    # 1. Skill Cleanup: Trigger recalculation for skills linked to the deleted document
    # Since the document is already removed from DB, count() will naturally decrease
    handle_skill_level(sender, document)

    # 2. Goal Resync: Refresh all goals to reflect potential drops in skill levels
    active_goals = Goal.objects.all()
    for goal in active_goals:
        updated_goal_score = goal.sync_with_existing_skills()
        Goal.objects(id=goal.id).update_one(set__current_score=updated_goal_score)

    # 3. Profile Update: Recalculate total years of experience and overall score
    user_profile = Profile.objects.first()
    if user_profile:
        # Reflect the loss of the deleted item in the global metrics
        current_exp = user_profile.calculate_total_experience()
        current_overall = user_profile.calculate_overall_score()

        Profile.objects(id=user_profile.id).update_one(
            set__experience_years=current_exp,
            set__overall_score=current_overall
        )

    # Audit log to track deletion sync
    deleted_model = sender.__name__.upper()
    print(f"🗑️ Delete Sync [SUCCESS]: {deleted_model} removed | System metrics updated.")


# --- Signal Registration Section ---
# List of models to monitor for any changes or deletions
models_to_watch = [Project, Course, Experience, Education, SelfStudy, Achievement, Goal, Skill]

for model in models_to_watch:
    # Connect saving events to the master sync logic
    signals.post_save.connect(master_sync_signal, sender=model)
    # Connect deletion events to the cleanup logic
    signals.post_delete.connect(master_delete_signal, sender=model)