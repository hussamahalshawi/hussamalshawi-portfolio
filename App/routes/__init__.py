from flask import Blueprint, render_template
from App.models import Profile, Project, Experience, Skill, Course, Goal

portfolio = Blueprint('portfolio', __name__)

@portfolio.route('/')
def index():
    try:
        # في MongoEngine نستخدم .objects.first() لجلب أول وثيقة
        # أو .objects() لجلب كل البيانات
        user_data = Profile.objects.first()
        skills_count = Skill.objects.count()
        courses_count = Course.objects.count()
        goals = Goal.objects.order_by('target_year')
        # جلب المشاريع والخبرات
        projects = Project.objects.all()
        experiences = Experience.objects.all()

        # إرسال البيانات للقالب
        return render_template('index.html',
                               user=user_data,
                               skills_count=skills_count,
                               courses_count=courses_count,
                               goals=goals,
                               projects=projects,
                               experiences=experiences)

    except Exception as e:
        print(f"Error fetching data: {e}")
        # تمرير كائنات فارغة لتجنب تعطل الصفحة (Graceful Degradation)
        return render_template('index.html', user=None, projects=[], experiences=[])

# @portfolio.route('/portfolio')
# def portfolio(): # هذا هو الاسم الذي يبحث عنه url_for
#     pass