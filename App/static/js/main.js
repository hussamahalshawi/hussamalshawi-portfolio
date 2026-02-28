// Initialize Animations
AOS.init({ duration: 1000, once: true });

/**
 * وظيفة التحكم بالوضع الليلي التلقائي واليدوي
 */
function applyTheme() {
    const html = document.documentElement;
    const icon = document.getElementById('theme-icon');
    const savedTheme = localStorage.getItem('theme');

    // 1. التحقق من وجود خيار يدوي سابق، وإلا نعتمد على إعدادات الجهاز
    const userPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme === 'dark' || (!savedTheme && userPrefersDark)) {
        html.classList.add('dark');
        if(icon) icon.classList.replace('fa-moon', 'fa-sun');
    } else {
        html.classList.remove('dark');
        if(icon) icon.classList.replace('fa-sun', 'fa-moon');
    }
}

// التبديل اليدوي عند الضغط على الزر
function toggleTheme() {
    const html = document.documentElement;
    const icon = document.getElementById('theme-icon');

    if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        html.classList.add('light');
        if(icon) icon.classList.replace('fa-sun', 'fa-moon');
        localStorage.setItem('theme', 'light');
    } else {
        html.classList.add('dark');
        html.classList.remove('light');
        if(icon) icon.classList.replace('fa-moon', 'fa-sun');
        localStorage.setItem('theme', 'dark');
    }
}

// تحديث أيقونة الزر عند تحميل الصفحة لكي تطابق الوضع التلقائي
document.addEventListener('DOMContentLoaded', () => {
    const icon = document.getElementById('theme-icon');
    if (document.documentElement.classList.contains('dark')) {
        if(icon) icon.classList.replace('fa-moon', 'fa-sun');
    }
});
// كود التحكم في قائمة الجوال
document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = menuButton.querySelector('i');

    menuButton.addEventListener('click', () => {
        // تبديل ظهور القائمة
        mobileMenu.classList.toggle('hidden');
        mobileMenu.classList.toggle('flex');

        // تغيير الأيقونة من Bars إلى X
        if (mobileMenu.classList.contains('hidden')) {
            menuIcon.classList.replace('fa-times', 'fa-bars');
        } else {
            menuIcon.classList.replace('fa-bars', 'fa-times');
        }
    });

    // إغلاق القائمة عند الضغط على أي رابط بداخلها
    mobileMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
            menuIcon.classList.replace('fa-times', 'fa-bars');
        });
    });
});
// أضف هذا الجزء لغلق المنيو تلقائياً عند تغيير حجم الشاشة
window.addEventListener('resize', () => {
    if (window.innerWidth >= 768) {
        const mobileMenu = document.getElementById('mobile-menu');
        const menuIcon = document.querySelector('#mobile-menu-button i');
        mobileMenu.classList.add('hidden');
        mobileMenu.classList.remove('flex');
        if(menuIcon) menuIcon.classList.replace('fa-times', 'fa-bars');
    }
});

function scrollToNextSection(element) {
    // العثور على السكشن الحالي الذي يحتوي على الزر
    const currentSection = element.closest('section');
    // العثور على السكشن الذي يليه مباشرة في الـ DOM
    const nextSection = currentSection.nextElementSibling;

    if (nextSection) {
        nextSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}
function filterProjects(category) {
    const cards = document.querySelectorAll('.project-card');
    const buttons = document.querySelectorAll('.filter-btn');

    // تحديث الأزرار
    buttons.forEach(btn => btn.classList.remove('active', 'bg-blue-600', 'text-white'));
    event.currentTarget.classList.add('active', 'bg-blue-600', 'text-white');

    cards.forEach(card => {
        const cardCat = card.getAttribute('data-category').trim();
        const cardIndex = parseInt(card.getAttribute('data-index'));

        if (category === 'all') {
            // عند اختيار الكل: أظهر أول 4 فقط وأخفِ الباقي (للحفاظ على جمالية الصفحة)
            if (cardIndex <= 4) {
                card.style.display = 'block';
                card.classList.remove('hidden-project');
            } else {
                card.style.display = 'none';
            }
        } else {
            // عند اختيار تصنيف معين: أظهر كل المشاريع التي تنتمي لهذا التصنيف
            if (cardCat === category) {
                card.style.display = 'block';
                card.classList.remove('hidden-project');
            } else {
                card.style.display = 'none';
            }
        }
    });
}

function filterAllProjects(category) {
    const cards = document.querySelectorAll('.project-card');
    const buttons = document.querySelectorAll('.filter-btn');

    // 1. تحديث الأزرار فوراً
    buttons.forEach(btn => {
        btn.classList.remove('active', 'bg-blue-600', 'text-white');
        btn.classList.add('text-slate-500');
    });
    event.currentTarget.classList.add('active', 'bg-blue-600', 'text-white');

    // 2. الفلترة مع حركة ناعمة جداً
    cards.forEach(card => {
        const cardCat = card.getAttribute('data-category').trim();

        // إخفاء العنصر بسلاسة أولاً
        card.style.opacity = '0';
        card.style.transform = 'scale(0.95)';

        setTimeout(() => {
            if (category === 'all' || cardCat === category) {
                card.style.display = 'block';
                // طلب إعادة رسم (Reflow) لضمان عمل الـ transition
                card.offsetHeight;
                card.style.opacity = '1';
                card.style.transform = 'scale(1)';
            } else {
                card.style.display = 'none';
            }
        }, 300); // مدة التلاشي
    });

    // 3. الأهم: تحديث AOS بعد انتهاء الحركة
    setTimeout(() => {
        AOS.refreshHard(); // يجبر AOS على إعادة حساب المواقع
    }, 400);
}
function fullSwapImage(thumbnailElement) {
    const mainImage = document.getElementById('main-project-image');

    // 1. حفظ المسارات الحالية
    const currentMainSrc = mainImage.src;
    const newMainSrc = thumbnailElement.src;

    // 2. تأثير حركي ناعم (Animation)
    mainImage.style.opacity = '0';
    thumbnailElement.style.opacity = '0';

    setTimeout(() => {
        // 3. التبديل الفعلي (Swap)
        mainImage.src = newMainSrc;            // المصغرة تصبح كبيرة
        thumbnailElement.src = currentMainSrc; // الكبيرة تصبح مصغرة

        // 4. إعادة الإظهار
        mainImage.style.opacity = '1';
        thumbnailElement.style.opacity = '1';
    }, 250);
}
//
//const feedbacksRaw = '{{ feedbacks_json | safe if feedbacks_json else '[]' }}';
//
//let feedbacks = [];
//try {
//    feedbacks = JSON.parse(feedbacksRaw);
//} catch (e) {
//    console.error("Error parsing feedback data:", e);
//    feedbacks = []; // مصفوفة فارغة في حال حدوث خطأ لمنع تعطل السكريبت
//}
//console.log("Feedbacks received from Server:", feedbacks);
//let feedbackIndex = 0;
//
//function showNextFeedback() {
//    if (feedbacks.length === 0) return;
//
//    const feedback = feedbacks[feedbackIndex];
//    const container = document.getElementById('feedback-toast-container');
//
//    // إنشاء عنصر الإشعار
//    const toast = document.createElement('div');
//    toast.className = "flex items-center gap-4 p-4 bg-white dark:bg-slate-900 shadow-2xl rounded-2xl border border-slate-200 dark:border-slate-800 transition-all duration-1000 opacity-0 translate-y-10 w-72 md:w-80 pointer-events-auto";
//
//    // داخل دالة showNextFeedback
//    toast.innerHTML = `
//    <div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0 shadow-lg shadow-blue-500/20">
//        <span class="text-white text-[10px] font-black">${feedback.person_name.charAt(0)}</span>
//    </div>
//    <div class="flex-1">
//        <div class="flex justify-between items-start">
//            <p class="text-[10px] font-black dark:text-white uppercase tracking-tighter">${feedback.person_name}</p>
//            <span class="text-[7px] text-slate-400 font-mono">${feedback.job_title}</span>
//        </div>
//        <p class="text-[9px] text-slate-500 dark:text-slate-400 mt-1 line-clamp-2 leading-relaxed">
//            "${feedback.feedback_text}"
//        </p>
//    </div>
//`;
//
//    container.appendChild(toast);
//
//    // أنيميشن الظهور (للوسط تقريباً)
//    setTimeout(() => {
//        toast.classList.remove('opacity-0', 'translate-y-10');
//        toast.classList.add('opacity-100', '-translate-y-4');
//    }, 100);
//
//    // أنيميشن الاختفاء بعد 5 ثواني
//    setTimeout(() => {
//        toast.classList.add('opacity-0', '-translate-y-20');
//        setTimeout(() => toast.remove(), 1000);
//    }, 5000);
//
//    // الانتقال للفيدباك التالي
//    feedbackIndex = (feedbackIndex + 1) % feedbacks.length;
//
//    // تكرار العملية كل 8 ثواني
//    setTimeout(showNextFeedback, 8000);
//}
//
//// بدء التشغيل عند تحميل الصفحة
//window.addEventListener('load', () => {
//    if(feedbacks.length > 0) {
//        setTimeout(showNextFeedback, 3000);
//    } else {
//        console.warn("No feedbacks to display in the toast system.");
//    }
//});