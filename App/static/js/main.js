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
/**
 * Opens the post detail modal and populates it with data.
 * Includes a fixed header with an action dropdown menu.
 * @param {string} postId - The unique ID of the post to fetch.
 */
async function openPostModal(postId) {
    const modal = document.getElementById('post-detail-modal');
    const content = document.getElementById('modal-content');


    modal.classList.remove('hidden');

    // Loading State
    content.innerHTML = `
        <div class="flex flex-col items-center justify-center p-20 space-y-4">
            <div class="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
            <p class="text-slate-500 font-bold animate-pulse uppercase text-xs tracking-widest">Loading Insight...</p>
        </div>
    `;

    try {
        const response = await fetch(`/api/posts/${postId}`);
        const post = await response.json();

        // External Link Button Logic
        const hasUrl = post.original_url && post.original_url !== '#' && post.original_url.trim() !== '';
        const urlButton = hasUrl
            ? `<a href="${post.original_url}" target="_blank" class="flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-full text-xs font-black uppercase tracking-widest hover:bg-blue-700 transition-all shadow-lg shadow-blue-500/20">
                View Original Post <i class="fas fa-external-link-alt text-[10px]"></i>
               </a>`
            : `<button disabled class="flex items-center gap-2 bg-slate-100 dark:bg-slate-800 text-slate-400 px-6 py-3 rounded-full text-xs font-black uppercase tracking-widest cursor-not-allowed">
                No External Link <i class="fas fa-lock text-[10px]"></i>
               </button>`;
// 1. تحديث الرابط فوراً ليصبح: website.com/blogs?post=123
    const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?post=' + postId;
    window.history.pushState({ path: newUrl }, '', newUrl);

    // 2. إظهار المودال
    const modal = document.getElementById('post-detail-modal');
    modal.classList.remove('hidden');
        // Building Modal Content with Fixed Header and Action Menu
        content.innerHTML = `
            <div class="sticky top-0 z-[100] bg-white dark:bg-slate-900 px-8 pt-8 pb-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
                <div class="flex items-center gap-4">
                    <span class="px-4 py-1.5 bg-blue-600 text-white text-[10px] font-black rounded-full uppercase tracking-[0.2em]">
                        # ${post.series_name || 'General'}
                    </span>
                    <span class="text-slate-400 text-[10px] font-bold uppercase tracking-widest italic">
                        ${post.date}
                    </span>
                </div>

                <div class="flex items-center gap-2">
                    <div class="relative inline-block text-left">
                        <button onclick="toggleModalOptions(event)"
                                class="w-10 h-10 rounded-xl bg-slate-50 dark:bg-slate-800 flex items-center justify-center text-slate-500 hover:bg-blue-600 hover:text-white transition-all">
                            <i class="fas fa-ellipsis-v text-sm"></i>
                        </button>

                        <div id="modal-dropdown-menu"
                             class="hidden absolute right-0 mt-2 w-48 origin-top-right bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700 rounded-2xl shadow-2xl z-[110] overflow-hidden">
                            <div class="py-1">
                                <button onclick="sharePost('${post.id}')" class="flex items-center gap-3 w-full px-4 py-3 text-[11px] font-black uppercase text-slate-600 dark:text-slate-300 hover:bg-blue-50 dark:hover:bg-blue-900/20 hover:text-blue-600 transition-all">
                                    <i class="fas fa-share-alt w-4"></i> Share Story
                                </button>
                            </div>
                        </div>
                    </div>

                    <button onclick="closePostModal()" class="w-10 h-10 rounded-xl text-slate-400 hover:text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-900/20 transition-all flex items-center justify-center">
                        <i class="fas fa-times text-xl"></i>
                    </button>
                </div>
            </div>

            <div class="p-8 space-y-8 overflow-y-auto max-h-[calc(90vh-100px)] custom-scrollbar" onclick="closeModalDropdown()">
                <div class="prose dark:prose-invert max-w-none text-slate-600 dark:text-slate-300 leading-relaxed text-lg font-medium">
                    ${post.content.replace(/\n/g, '<br>')}
                </div>

                ${post.image ? `
                    <div class="rounded-[2.5rem] overflow-hidden shadow-2xl bg-slate-50 dark:bg-slate-800/20 border border-slate-100 dark:border-slate-800">
                        <img src="${post.image}" class="w-full h-auto block">
                    </div>
                ` : ''}

                ${post.tags && post.tags.length > 0 ? `
                    <div class="flex flex-wrap gap-2">
                        ${post.tags.map(tag => `<span class="text-[10px] font-bold text-blue-500 bg-blue-50 dark:bg-blue-900/20 px-3 py-1 rounded-md">#${tag}</span>`).join('')}
                    </div>
                ` : ''}

                <div class="pt-8 border-t border-slate-100 dark:border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-6 pb-2">
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

        // Update view count in feed background
        const viewSpan = document.getElementById(`view-count-${postId}`);
        if(viewSpan) viewSpan.innerText = post.views;

    } catch (err) {
        content.innerHTML = `<div class="p-10 text-center text-rose-500 font-bold">Failed to load content. Please try again.</div>`;
        console.error("[Error]: Modal loading failed", err);
    }
}

/**
 * Toggles the dropdown menu inside the Modal.
 */
function toggleModalOptions(event) {
    event.stopPropagation();
    const menu = document.getElementById('modal-dropdown-menu');
    menu.classList.toggle('hidden');
}

/**
 * Closes the dropdown menu if clicking inside the body content.
 */
function closeModalDropdown() {
    const menu = document.getElementById('modal-dropdown-menu');
    if (menu) menu.classList.add('hidden');
}
/**
 * Shares the post or copies the link with error handling and fallback.
 * @param {string} postId - Unique post identifier.
 */
/**
 * Shares the post using the device's native sharing mechanism.
 * Falls back to clipboard copy if native sharing is unavailable.
 * @param {string} postId - The unique ID of the post.
 */
async function sharePost(postId) {
    // 1. Close the dropdown menu first
    const menu = document.getElementById(`card-menu-${postId}`);
    if (menu) menu.classList.add('hidden');

    // 2. Prepare the data (Ensure this matches your Flask route)
    const postUrl = `${window.location.origin}/blogs?post=${postId}`;
    const shareData = {
        title: 'Hussam Alshawi - Programming Insight',
        text: 'Check out this technical insight from Hussam Alshawi\'s portfolio!',
        url: postUrl
    };

    try {
        // 3. Primary: Try Web Share API (Opens native mobile/desktop share menu)
        if (navigator.share) {
            await navigator.share(shareData);
            console.log(`[Log]: Post ${postId} shared via Native API.`);
        } else {
            throw new Error('Native share not supported');
        }
    } catch (err) {
        // 4. Fallback: Manual Copy to Clipboard
        try {
            await navigator.clipboard.writeText(postUrl);

            // Show a visual feedback toast instead of a boring alert
            showShareToast("Link copied to clipboard!");
            console.log(`[Log]: Post ${postId} copied to clipboard (Fallback).`);
        } catch (copyErr) {
            console.error(`[Error]: Critical failure in sharing: ${copyErr}`);
        }
    }
}

/**
 * Displays a non-intrusive notification toast.
 * @param {string} message
 */
function showShareToast(message) {
    const toast = document.createElement('div');
    toast.className = "fixed bottom-10 left-1/2 -translate-x-1/2 bg-blue-600 text-white px-8 py-3 rounded-full text-[11px] font-black uppercase tracking-[0.2em] z-[999] shadow-2xl animate-pulse";
    toast.innerText = message;
    document.body.appendChild(toast);

    // Remove toast after 3 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.5s ease';
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}


// وظيفة فتح/إغلاق القائمة لكل منشور بشكل مستقل
function toggleCardOptions(postId, event) {
    event.stopPropagation(); // منع فتح المودال

    // 1. تحديد المنشور الحالي والمنشورات الأخرى
    const currentCard = event.target.closest('.post-card');
    const allCards = document.querySelectorAll('.post-card');
    const menu = document.getElementById(`card-menu-${postId}`);

    // 2. إغلاق أي قائمة مفتوحة وإعادة Z-index لكل البطاقات للوضع الطبيعي
    allCards.forEach(card => {
        card.style.zIndex = "10"; // الوضع الافتراضي
        const otherMenu = card.querySelector('[id^="card-menu-"]');
        if (otherMenu && otherMenu.id !== `card-menu-${postId}`) {
            otherMenu.classList.add('hidden');
        }
    });

    // 3. تبديل حالة القائمة الحالية
    const isHidden = menu.classList.contains('hidden');

    if (isHidden) {
        menu.classList.remove('hidden');
        currentCard.style.zIndex = "50"; // رفع المنشور الحالي فوق الجميع
    } else {
        menu.classList.add('hidden');
        currentCard.style.zIndex = "10"; // إعادة المنشور لوضعه الطبيعي
    }
}

// تشغيل الكود بمجرد تحميل الصفحة بالكامل
document.addEventListener('DOMContentLoaded', function() {
    // 1. قراءة المعايير (Parameters) من الرابط (URL)
    const urlParams = new URLSearchParams(window.location.search);
    const postId = urlParams.get('post'); // سيبحث عن كلمة ?post=123

    // 2. إذا وجد ID لمنشور، قم بفتح المودال تلقائياً
    if (postId) {
        // ننتظر قليلاً لضمان تحميل بقية العناصر أو الـ DOM
        setTimeout(() => {
            if (typeof openPostModal === 'function') {
                openPostModal(postId);
            }
        }, 500); // تأخير بسيط 500ms لضمان استقرار الصفحة
    }
});
// فتح وإغلاق القائمة
function togglePostOptions() {
    const menu = document.getElementById('dropdown-menu');
    menu.classList.toggle('hidden');
}

// إغلاق القائمة عند النقر خارجها
function closeDropdownIfOpen() {
    const menu = document.getElementById('dropdown-menu');
    if (!menu.classList.contains('hidden')) {
        menu.classList.add('hidden');
    }
}
function closePostModal() {
    const modal = document.getElementById('post-detail-modal');
    modal.classList.add('hidden');

    // إعادة الرابط لشكلة الطبيعي: website.com/blogs
    const cleanUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
    window.history.replaceState({ path: cleanUrl }, '', cleanUrl);
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

// 1. تفعيل اختيار الملفات عند الضغط على الأيقونة
function triggerFileInput() {
    document.getElementById('post-image-input').click();
}

// 2. معاينة الصورة المختارة
function previewImage(input) {
    const container = document.getElementById('image-preview-container');
    const preview = document.getElementById('image-preview');

    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            container.classList.remove('hidden');
        }
        reader.readAsDataURL(input.files[0]);
    }
}

// 3. حذف الصورة المختارة
function removeSelectedImage() {
    document.getElementById('post-image-input').value = "";
    document.getElementById('image-preview-container').classList.add('hidden');
}

// دالة عامة لإضافة الوسوم حول النص المحدد
function insertTag(tagName) {
    const textarea = document.getElementById('post-content');
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = textarea.value.substring(start, end);

    // إذا لم يتم تحديد نص، نضع نصاً افتراضياً
    const content = selectedText || (tagName === 'li' ? 'List item' : 'Text');
    const replacement = `<${tagName}>${content}</${tagName}>`;

    textarea.value = textarea.value.substring(0, start) + replacement + textarea.value.substring(end);
    textarea.focus();
}

// دالة خاصة بالكود (لأنه يحتاج pre و code معاً)
function insertCodeTag() {
    const textarea = document.getElementById('post-content');
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = textarea.value.substring(start, end);

    const replacement = `<pre><code>${selectedText || 'Code here...'}</code></pre>`;

    textarea.value = textarea.value.substring(0, start) + replacement + textarea.value.substring(end);
    textarea.focus();
}
document.getElementById('add-post-form').addEventListener('submit', async (e) => {
    e.preventDefault(); // منع الصفحة من التحديث التلقائي

    // 1. إنشاء حاوية البيانات (FormData) لدعم رفع الملفات والنصوص معاً
    const formData = new FormData();

    // 2. إضافة النصوص من المدخلات (حسب الـ IDs الموجودة في الفورم المرتب)
    formData.append('content', document.getElementById('post-content').value);
    formData.append('series_id', document.getElementById('post-series').value);
    formData.append('original_url', document.getElementById('post-url').value);
    formData.append('tags', document.getElementById('post-tags').value);

    // 3. التحقق من وجود صورة وإضافتها
    const fileInput = document.getElementById('post-image-input');
    if (fileInput.files[0]) {
        formData.append('image', fileInput.files[0]);
    }

    try {
        // 4. الإرسال إلى السيرفر
        const response = await fetch('/api/posts/create', {
            method: 'POST',
            body: formData // ملاحظة: لا نضع Headers يدوية هنا، المتصفح سيتكفل بها
        });

        const result = await response.json();

        if (response.ok) {
            // نجاح العملية
            Swal.fire({
                icon: 'success',
                title: 'Published!',
                text: 'Your insight has been posted successfully.',
                timer: 2000,
                showConfirmButton: false
            });

            e.target.reset(); // تفريغ الفورم
            setTimeout(() => location.reload(), 2100); // تحديث الصفحة لرؤية المنشور الجديد
        } else {
            // في حال وجود خطأ من السيرفر
            Swal.fire('Error', result.message || 'Something went wrong', 'error');
        }
    } catch (error) {
        console.error("Submission failed:", error);
        Swal.fire('Error', 'Connection failed', 'error');
    }
});