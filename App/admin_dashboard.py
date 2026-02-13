from flask_admin import AdminIndexView, expose
from App.models.skill import Skill, SkillType
from App.models.goal import Goal
from App.models.profile import Profile
from App.models.course import Course
import json
import logging


class ProfessionalDashboardView(AdminIndexView):
    """
    HussamAlshawi-Portfolio Professional Dashboard.
    Ensures zero-crash logic by validating every model query.
    """

    @expose('/')
    def index(self):
        try:
            # 1. Profile Data Sync (Safe Check)
            # We use .first() and handle the case if the profile is None
            user_profile = Profile.objects.first()

            # Using getattr to safely fetch fields even if they don't exist yet
            avg_goal_score = getattr(user_profile, 'overall_score', 0) if user_profile else 0
            years_exp = getattr(user_profile, 'experience_years', 0) if user_profile else 0

            # 2. Learning Hours Calculation
            # We wrap this in a sub-try to prevent it from crashing the whole dashboard
            try:
                total_hours = Course.objects.sum('hours_spent') or 0
            except Exception:
                total_hours = 0

            # 3. Skills Distribution (Chart Data)
            all_types = SkillType.objects.all()
            skills_labels = [t.name for t in all_types] if all_types else []
            skills_counts = [Skill.objects(skill_type=t).count() for t in all_types] if all_types else []

            # 4. Goals Performance (Chart Data)
            all_goals = Goal.objects.all().order_by('target_year')
            goals_labels = [g.goal_name for g in all_goals] if all_goals else []
            goals_scores = [g.current_score if g.current_score else 0 for g in all_goals] if all_goals else []

            return self.render(
                'admin/hussam_dashboard.html',
                skills_labels=json.dumps(skills_labels),
                skills_counts=json.dumps(skills_counts),
                goals_labels=json.dumps(goals_labels),
                goals_scores=json.dumps(goals_scores),
                total_skills_count=Skill.objects.count(),
                avg_goal_score=avg_goal_score,
                total_hours_spent=total_hours,
                years_of_experience=years_exp
            )
        except Exception as e:
            # This will print the EXACT error in your terminal
            logging.error(f"DEBUG: Dashboard Sync failed due to: {str(e)}")
            # Show the actual error to the user during development
            return self.render('admin/hussam_dashboard.html', error_message=f"Sync Error: {str(e)}")