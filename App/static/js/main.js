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
async function handleLike(postId, btnElement) {
    try {
        const response = await fetch(`/api/posts/${postId}/like`, { method: 'POST' });
        const data = await response.json();

        if (response.ok) {
            // تحديث الرقم في الواجهة
            const countSpan = btnElement.querySelector('.like-count');
            countSpan.innerText = data.new_likes;

            // تغيير شكل القلب وتأثير لوني
            const icon = btnElement.querySelector('i');
            icon.classList.replace('far', 'fas');
            icon.classList.add('text-rose-500', 'animate-bounce');
            btnElement.classList.add('text-rose-500');

            // تعطيل الزر لمنع الإعجاب المتكرر في نفس الجلسة (اختياري)
            btnElement.onclick = null;
        }
    } catch (error) {
        console.error("Like failed:", error);
    }
}
document.addEventListener('DOMContentLoaded', () => {
    // إعدادات المراقب
    const options = {
        root: null, // استخدام شاشة المتصفح كمرجع
        threshold: 0.6 // احتساب المشاهدة عند ظهور 60% من الكرت
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const postId = entry.target.getAttribute('data-post-id');

                // إرسال الطلب للـ API في الخلفية
                incrementView(postId);

                // التوقف عن مراقبة هذا العنصر لعدم تكرار الزيادة في نفس الجلسة
                observer.unobserve(entry.target);
            }
        });
    }, options);

    // تفعيل المراقب على جميع كروت المقالات
    document.querySelectorAll('.post-card').forEach(card => {
        observer.observe(card);
    });
});

async function incrementView(postId) {
    try {
        const response = await fetch(`/api/posts/${postId}/view`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await response.json();

        if (response.ok) {
            // تحديث الرقم في الواجهة لحظياً
            const viewSpan = document.getElementById(`view-count-${postId}`);
            if (viewSpan) {
                viewSpan.innerText = data.new_views;
            }
        }
    } catch (error) {
        console.error("Tracking Error:", error);
    }
}

async function openPostModal(postId) {
    const modal = document.getElementById('post-detail-modal');
    const content = document.getElementById('modal-content');

    modal.classList.remove('hidden');
    content.innerHTML = '<div class="text-center p-10"><i class="fas fa-spinner animate-spin text-3xl text-blue-600"></i></div>';

    try {
        const response = await fetch(`/api/posts/${postId}`);
        const post = await response.json();

        content.innerHTML = `
            <button onclick="closePostModal()" class="absolute top-6 right-6 text-slate-400 hover:text-red-500"><i class="fas fa-times text-2xl"></i></button>
            <div class="space-y-6">
                <span class="text-blue-600 text-xs font-black uppercase tracking-widest">${post.date}</span>
                <h1 class="text-3xl md:text-4xl font-[1000] dark:text-white leading-tight">${post.title}</h1>
                ${post.image ? `<img src="${post.image}" class="w-full rounded-2xl shadow-lg">` : ''}
                <div class="prose dark:prose-invert max-w-none text-slate-600 dark:text-slate-300 leading-relaxed text-lg">
                    ${post.content}
                </div>
            </div>
        `;

        // تحديث عداد المشاهدات في الصفحة الرئيسية أيضاً
        const viewSpan = document.getElementById(`view-count-${postId}`);
        if(viewSpan) viewSpan.innerText = post.views;

    } catch (err) {
        content.innerHTML = '<p class="text-red-500">Failed to load post.</p>';
    }
}

function closePostModal() {
    document.getElementById('post-detail-modal').classList.add('hidden');
}
document.getElementById('add-post-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
        title: document.getElementById('post-title').value,
        series_id: document.getElementById('post-series').value,
        content: document.getElementById('post-content').value,
        original_url: document.getElementById('post-url').value,
        tags: document.getElementById('post-tags').value
    };

    try {
        const response = await fetch('/api/posts/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            Swal.fire({ icon: 'success', title: 'Success!', text: 'Post Published', timer: 1500 });
            e.target.reset();
            setTimeout(() => location.reload(), 1600);
        }
    } catch (error) {
        console.error("Error:", error);
    }
});