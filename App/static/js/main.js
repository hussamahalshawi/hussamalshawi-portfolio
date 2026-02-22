// Initialize Animations
AOS.init({ duration: 1000, once: true });

// Theme Toggle Logic
function toggleTheme() {
    const html = document.documentElement;
    const icon = document.getElementById('theme-icon');

    if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        icon.classList.replace('fa-sun', 'fa-moon');
        localStorage.setItem('theme', 'light');
    } else {
        html.classList.add('dark');
        icon.classList.replace('fa-moon', 'fa-sun');
        localStorage.setItem('theme', 'dark');
    }
}

// Apply theme on Page Load
(function() {
    const savedTheme = localStorage.getItem('theme');
    const icon = document.getElementById('theme-icon');
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
        if(icon) icon.classList.replace('fa-moon', 'fa-sun');
    }
})();