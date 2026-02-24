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