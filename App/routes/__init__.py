from flask import Blueprint, render_template, redirect, url_for
from App.models import Profile, Project, Experience, Skill, Course, Goal, Category

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
        projects = Project.objects.order_by('-id').all()
        # 1. جلب الفئات من قاعدة البيانات
        db_categories = Category.objects.all()

        # 2. تعريف الترتيب الذي تريده بالضبط
        custom_order = [
            'Python Development',
            'Web Development',
            'Data Structures',
            'Data Analysis',
            'Problem Solving',
            'Artificial Intelligence',
            'Mobile Development',
            'Software Engineering'
        ]

        # 3. ترتيب الفئات بناءً على القائمة أعلاه
        # سيتم وضع أي فئة غير موجودة في القائمة في نهاية المتصفح
        sorted_categories = sorted(db_categories,
                                   key=lambda x: custom_order.index(x.name) if x.name in custom_order else 999)
        experiences = Experience.objects.all()

        # إرسال البيانات للقالب
        return render_template('index.html',
                               user=user_data,
                               skills_count=skills_count,
                               courses_count=courses_count,
                               goals=goals,
                               projects=projects,
                               categories=sorted_categories,
                               experiences=experiences)

    # في بلوك الـ except داخل routes/__init__.py

    except Exception as e:

        print(f"Error fetching data: {e}")

        # تمرير قيم افتراضية آمنة تمنع Jinja2 من الانهيار

        return render_template('index.html',

                               user={'overall_score': 0},

                               projects=[],

                               experiences=[],

                               goals=[],

                               skills_count=0,

                               courses_count=0)


@portfolio.route('/projects')
def all_projects():
    """
    عرض صفحة أرشيف المشاريع الكاملة
    يتم جلب جميع المشاريع مرتبة من الأحدث إلى الأقدم
    """
    try:
        # 1. جلب جميع المشاريع من قاعدة البيانات وترتيبها (الأحدث أولاً)
        # الترتيب حسب '-id' أو '-created_at' يضمن ظهور آخر عمل قمت به في البداية
        projects = Project.objects.order_by('-id').all()

        # 2. جلب جميع التصنيفات لغايات الفلترة في الصفحة
        categories = Category.objects.all()

        # 3. تعريف الترتيب المخصص للتصنيفات (اختياري كما فعلنا سابقاً)
        custom_order = [
            'Python Development', 'Web Development', 'Data Structures',
            'Data Analysis', 'Problem Solving', 'Artificial Intelligence',
            'Mobile Development', 'Software Engineering'
        ]

        # ترتيب التصنيفات برمجياً بناءً على القائمة أعلاه
        sorted_categories = sorted(
            categories,
            key=lambda x: custom_order.index(x.name.strip()) if x.name.strip() in custom_order else 999
        )

        # 4. رندر الصفحة وإرسال البيانات
        return render_template(
            'projects.html',
            projects=projects,
            categories=sorted_categories,
            title="Project Archive | Hussam Alshawi"
        )

    except Exception as e:
        # التعامل مع الخطأ في حال تعذر جلب البيانات من MongoDB
        print(f"Error fetching projects: {e}")
        return render_template('errors/500.html'), 500


@portfolio.route('/project/<project_id>')
def project_details(project_id):
    try:
        # البحث عن المشروع باستخدام المعرف النصي
        project = Project.objects.get(id=project_id)
        return render_template('project_details.html', project=project)
    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for('portfolio.index'))
