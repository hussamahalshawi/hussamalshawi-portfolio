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
    // حالة التحميل
    content.innerHTML = `
        <div class="flex flex-col items-center justify-center p-20 space-y-4">
            <div class="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            <p class="text-slate-500 font-bold animate-pulse uppercase text-xs tracking-widest">Loading Insight...</p>
        </div>
    `;

    try {
        const response = await fetch(`/api/posts/${postId}`);
        const post = await response.json();

        // منطق زر الرابط الأصلي
        const hasUrl = post.original_url && post.original_url !== '#' && post.original_url.trim() !== '';
        const urlButton = hasUrl
            ? `<a href="${post.original_url}" target="_blank" class="flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-full text-xs font-black uppercase tracking-widest hover:bg-blue-700 transition-all shadow-lg shadow-blue-500/20">
                View Original Post <i class="fas fa-external-link-alt text-[10px]"></i>
               </a>`
            : `<button disabled class="flex items-center gap-2 bg-slate-100 dark:bg-slate-800 text-slate-400 px-6 py-3 rounded-full text-xs font-black uppercase tracking-widest cursor-not-allowed">
                No External Link <i class="fas fa-lock text-[10px]"></i>
               </button>`;

        // بناء محتوى المودال
        content.innerHTML = `
            <button onclick="closePostModal()" class="absolute top-6 right-6 text-slate-400 hover:text-rose-500 transition-colors z-10">
                <i class="fas fa-times text-2xl"></i>
            </button>

            <div class="space-y-8">
                <div class="flex flex-wrap items-center gap-4">
                    <span class="px-4 py-1.5 bg-blue-600 text-white text-[10px] font-black rounded-full uppercase tracking-[0.2em]">
                        # ${post.series_name || 'General'}
                    </span>
                    <span class="text-slate-400 text-[10px] font-bold uppercase tracking-widest italic">
                        ${post.date}
                    </span>
                </div>

                <h1 class="text-3xl md:text-5xl font-[1000] text-slate-900 dark:text-white leading-[1.1] tracking-tighter">
                    ${post.title}
                </h1>

                ${post.image ? `
                    <div class="rounded-[2rem] overflow-hidden shadow-2xl">
                        <img src="${post.image}" class="w-full h-auto object-cover max-h-[500px]">
                    </div>
                ` : ''}

                ${post.tags && post.tags.length > 0 ? `
                    <div class="flex flex-wrap gap-2">
                        ${post.tags.map(tag => `<span class="text-[10px] font-bold text-blue-500 bg-blue-50 dark:bg-blue-900/20 px-3 py-1 rounded-md">#${tag}</span>`).join('')}
                    </div>
                ` : ''}

                <div class="prose dark:prose-invert max-w-none text-slate-600 dark:text-slate-300 leading-relaxed text-lg font-medium">
                    ${post.content.replace(/\n/g, '<br>')}
                </div>

                <div class="pt-8 border-t border-slate-100 dark:border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-6">
                    <div class="flex items-center gap-8">
                        <div class="flex flex-col">
                            <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Views</span>
                            <span class="text-xl font-black dark:text-white">${post.views}</span>
                        </div>
                        <div class="flex flex-col">
                            <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Likes</span>
                            <span class="text-xl font-black dark:text-white">${post.likes}</span>
                        </div>
                    </div>
                    ${urlButton}
                </div>
            </div>
        `;

        // تحديث العداد في الخلفية (Feed)
        const viewSpan = document.getElementById(`view-count-${postId}`);
        if(viewSpan) viewSpan.innerText = post.views;

    } catch (err) {
        content.innerHTML = `<div class="p-10 text-center text-rose-500 font-bold">Failed to load content. Please try again.</div>`;
    }
}

function closePostModal() {
    document.getElementById('post-detail-modal').classList.add('hidden');
}
document.getElementById('add-post-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const rawTags = document.getElementById('post-tags').value;
    const tagsArray = rawTags.split(',')
                             .map(tag => tag.trim()) // إزالة المسافات الزائدة
                             .filter(tag => tag !== ""); // إزالة المدخلات الفارغة
    const payload = {
        title: document.getElementById('post-title').value,
        series_id: document.getElementById('post-series').value,
        content: document.getElementById('post-content').value,
        original_url: document.getElementById('post-url').value,
        tags: tagsArray
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
    console.log("Sending Tags:", tagsArray);
});