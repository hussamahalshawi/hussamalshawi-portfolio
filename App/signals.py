from App.models.project import Project
from App.models.course import Course
from App.models.experience import Experience
from App.models.education import Education
from App.models.self_study import SelfStudy
from App.models.achievement import Achievement
from App.models.skill import SkillType
from App.models.skill import Skill
from mongoengine import signals


def update_skill_logic(sender, document, **kwargs):
    skill_to_process = []

    if isinstance(document, Project) and document.skills_used:
        skill_to_process = [(s, 10) for s in document.skills_used]

    elif isinstance(document, Course) and document.acquired_skills:
        skill_to_process = [(s, 15) for s in document.acquired_skills]
    elif isinstance(document, Experience) and document.skills_acquired:
        skill_to_process = [(s, 20) for s in document.skills_acquired]
    elif isinstance(document, Education) and document.skills_learned:
        skill_to_process = [(s, 5) for s in document.skills_learned]
    elif isinstance(document, SelfStudy) and document.skills_learned:
        skill_to_process = [(s, 8) for s in document.skills_learned]
    elif isinstance(document, Achievement) and document.skills_demonstrated:
        skill_to_process = [(s, 30) for s in document.skills_demonstrated]

    for skill_name, weight in skill_to_process:
        skill = Skill.objects(skill_name__iexact=skill_name.strip()).first()
        if not skill:
            skill = Skill(skill_name=skill_name.strip(), skill_type=auto_assign_skilltype(skill_name), level=0)

        skill.level = min(skill.level + weight, 100)
        skill.save()






def auto_assign_skilltype(skill_name):
    skill_name_upper = skill_name.upper().strip()

    types = SkillType.objects.all()

    for s_type in types:
        if skill_name_upper in [s.upper() for s in s_type.keywords]:
            return s_type
    default_type = SkillType.objects(name__iexact="Other technologies").first()
    if default_type:
        return default_type
    return None


# src/signals.py

def remove_skill_logic(sender, document, **kwargs):
    skills_to_reduce = []

    # 1. تحديد الوزن الذي يجب خصمه بناءً على الموديل المحذوف
    if isinstance(document, Project) and hasattr(document, 'skills_used') and document.skills_used:
        skills_to_reduce = [(s, 10) for s in document.skills_used]

    elif isinstance(document, Course) and hasattr(document, 'acquired_skills') and document.acquired_skills:
        skills_to_reduce = [(s, 15) for s in document.acquired_skills]

    elif isinstance(document, Experience) and hasattr(document, 'skills_acquired') and document.skills_acquired:
        skills_to_reduce = [(s, 20) for s in document.skills_acquired]

    # ... أضف باقي الموديلات (Education, SelfStudy, etc.) بنفس الأوزان التي استخدمتها في الإضافة ...

    # 2. معالجة الخصم أو الحذف
    for skill_name, weight in skills_to_reduce:
        name_clean = skill_name.strip()
        skill = Skill.objects(skill_name__iexact=name_clean).first()

        if skill:
            # خصم الوزن من المستوى الحالي
            new_level = max((skill.level or 0) - weight, 0)

            if new_level <= 0:
                # إذا وصل المستوى لـ 0، نحذف المهارة تماماً
                skill.delete()
                print(f"🗑️ تم حذف المهارة بالكامل: {name_clean}")
            else:
                # إذا لا يزال هناك مستوى، نقوم بتحديثه فقط
                skill.level = new_level
                skill.save()
                print(f"📉 تم تقليل مستوى المهارة {name_clean} إلى {new_level}%")


def update_goal_scoring(sender, document, **kwargs):
    from App.models.goal import Goal

    model_skills_map = {
        'Project': 'skills_used',
        'Course': 'acquired_skills',
        'Experience': 'skills_acquired',
        'Education': 'skills_learned',
        'SelfStudy': 'skills_learned',
        'Achievement': 'skills_demonstrated'
    }

    # 2. استخراج المهارات بناءً على نوع الموديل (sender)
    model_name = sender.__name__
    skills_field = model_skills_map.get(model_name)

    # جلب قائمة المهارات من الوثيقة باستخدام getattr
    skills_in_doc = getattr(document, skills_field, []) if skills_field else []

    if not skills_in_doc:
        return

    # 3. تنظيف المهارات وتجهيزها للمقارنة
    skills_in_doc_lower = [s.lower().strip() for s in skills_in_doc]

    # 4. تحديث الأهداف المرتبطة
    all_goals = Goal.objects.all()
    for goal in all_goals:
        # تحويل مهارات الهدف للور كيس للمقارنة العادلة
        goal_skills_lower = [gs.lower().strip() for gs in goal.required_skills]

        # التأكد من وجود تقاطع (Intersection) بين مهارات الإنجاز ومهارات الهدف
        has_match = any(skill in goal_skills_lower for skill in skills_in_doc_lower)

        if has_match:
            # زيادة السكور (مثلاً 10 نقاط للمشاريع و 5 للكورسات)
            points = 5 if model_name == 'Project' else 25
            goal.current_score = min(goal.current_score + points, goal.target_score)
            goal.save()

models_to_watch = [Project, Course, Experience, Education, SelfStudy, Achievement]

for model in models_to_watch:
    # نحن هنا نقول لـ MongoEngine: "عند حفظ أي وثيقة من هذه الموديلات، نادِ دالة update_skill_logic"
    signals.post_save.connect(update_skill_logic, sender=model)
    signals.post_save.connect(update_goal_scoring, sender=model)
    signals.post_delete.connect(remove_skill_logic, sender=model)