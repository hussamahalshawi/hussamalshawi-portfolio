from flask import Blueprint, render_template, redirect, url_for
from App.models import Profile, Project, Experience, Skill, Course, Goal, Category, Language, Education, SelfStudy, Achievement, Feedback, SkillType, Post, Series
from flask import request, jsonify
import json
from datetime import datetime, timezone

portfolio = Blueprint('portfolio', __name__)


@portfolio.context_processor
def inject_user_data():
    """
    يقوم هذا الكود بحقن بيانات المستخدم في جميع القوالب تلقائياً.
    سيكون متغير 'user' متاحاً في كل الصفحات دون الحاجة لتمريره في الـ route.
    """

    # جلب بياناتك (بما أنك صاحب البورتفوليو، غالباً هناك سجل واحد فقط)
    user_data = Profile.objects.first()

    # يمكنك أيضاً جلب أعداد المهارات أو الكورسات هنا إذا كانت تظهر في base.html
    return dict(user=user_data)

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
        languages = Language.objects.all().order_by('-level')

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
        courses = Course.objects.all()
        educations = Education.objects.all()
        selfstudys = SelfStudy.objects.all()
        target_categories = ["Programming languages",
                             "Frameworks",
                             "Database",
                             "Soft skills",
                             "API (Web Technologies & APIs)",
                             "DevOps & Cloud",
                             "AI & Data Science",
                             "Business",
                             "Technical Skills",
                             "Artificial Intelligence"]

        # 2. جلب الـ IDs الخاصة بهذه الأنواع أولاً
        selected_types = SkillType.objects(name__in=target_categories)

        # 3. جلب المهارات التي تنتمي لهذه الأنواع فقط، مرتبة تنازلياً حسب السكور
        # نستخدم [:10] لجلب أعلى 10 فقط كما في الكود الخاص بك
        skills = Skill.objects(skill_type__in=selected_types, level__gt=75).order_by('skill_type', '-level')[:10]
        achievements = Achievement.objects.all()
        feedbacks = Feedback.objects.all()

        # إرسال البيانات للقالب
        return render_template('index.html',
                               user=user_data,
                               skills_count=skills_count,
                               courses_count=courses_count,
                               goals=goals,
                               projects=projects,
                               categories=sorted_categories,
                               languages=languages,
                               courses=courses,
                               educations=educations,
                               selfstudys=selfstudys,
                               skills=skills,
                               achievements=achievements,
                               feedbacks=feedbacks,
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


@portfolio.context_processor
def inject_feedbacks():
    try:
        # 1. جلب البيانات والتأكد من أنها ليست فارغة
        feedbacks_query = Feedback.objects.all().order_by('-created_at')

        # 2. تحويلها يدوياً لمصفوفة بسيطة (Plain Dictionary)
        feedbacks_list = []
        for f in Feedback.objects.all():
            feedbacks_list.append({
                "person_name": f.person_name,
                "job_title": f.job_title or "Professional",
                "feedback_text": f.feedback_text,
                "contact_email": f.contact_email,
                "linkedin_url": getattr(f, 'linkedin_url', ""),  # استخدام getattr للأمان
                "created_at": f.created_at.isoformat() if f.created_at else ""
            })

        # إرسالها للقالب
        return dict(feedbacks_json=json.dumps(feedbacks_list))
    except Exception as e:
        print(f"CRITICAL ERROR in context_processor: {e}")
        return dict(feedbacks_json="[]")


@portfolio.route('/skills')
def all_skills():
    """
    Route to display all technical skills ordered by proficiency level.
    Adheres to HussamAlshawi-Portfolio clean code standards.
    """
    try:
        # جلب المهارات مرتبة تنازلياً حسب السكور
        # إذا كنت تستخدم SQLAlchemy: Skill.query.order_by(Skill.level.desc()).all()
        # إذا كنت تستخدم MongoEngine: Skill.objects.order_by('-level')
        all_skills = Skill.objects.order_by('-level')
        skill_types = SkillType.objects.all()

        # حساب إحصائيات سريعة لتعزيز الـ SEO والمحتوى
        total_count = all_skills.count()

        return render_template('skills_page.html',
                               skills=all_skills,
                               total_count=total_count,
                               skill_types=skill_types,
                               title="Technical Stack | All Skills")
    except Exception as e:
        # معالجة الخطأ بشكل نظيف
        print(f"Error fetching skills: {e}")
        return redirect(url_for('index'))


@portfolio.route('/blogs')
def blogs():
    # جلب جميع المنشورات وترتيبها حسب التاريخ (الأحدث أولاً)
    posts = Post.objects.order_by('-created_at')
    # جلب السلاسل لغرض التصفية (Filtering) في الصفحة
    series_list = Series.objects.all()

    return render_template('blogs.html', posts=posts, series_list=series_list)


@portfolio.route('/api/feedback', methods=['POST'])
def add_feedback():
    try:
        data = request.get_json()

        # التحقق من البيانات (Validation) بناءً على قيود المودل
        if not data.get('person_name') or not data.get('contact_email'):
            return jsonify({"status": "error", "message": "Name and Email are required!"}), 400

        # إنشاء سجل جديد في قاعدة البيانات
        new_feedback = Feedback(
            person_name=data.get('person_name'),
            job_title=data.get('job_title', 'Client/Colleague'),
            feedback_text=data.get('feedback_text'),
            contact_email=data.get('contact_email'),
            linkedin_url=data.get('linkedin_url', '')
        )

        # حفظ السجل
        new_feedback.save()

        return jsonify({
            "status": "success",
            "message": f"Thank you {new_feedback.person_name}, your feedback has been saved!"
        }), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@portfolio.route('/api/posts/<post_id>/like', methods=['POST'])
def like_post(post_id):
    try:
        post = Post.objects.get(id=post_id)
        post.likes_count = (post.likes_count or 0) + 1
        post.save()
        return jsonify({"status": "success", "new_likes": post.likes_count}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 404
