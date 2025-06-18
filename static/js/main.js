// main.js (core layout + utilities)
document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const menuButton = document.querySelector('.mobile-menu-button');

    if (sidebar && mainContent && menuButton) {
        window.toggleSidebar = function () {
            if (window.innerWidth <= 1024) {
                const isCollapsed = !sidebar.classList.contains('show');
                sidebar.classList.toggle('show');
                menuButton.setAttribute('aria-expanded', isCollapsed ? 'true' : 'false');
                mainContent.style.pointerEvents = isCollapsed ? 'none' : 'auto';
            } else {
                sidebar.classList.toggle('collapsed');
                mainContent.classList.toggle('collapsed-sidebar');
            }
        };

        mainContent.addEventListener('click', () => {
            if (window.innerWidth <= 1024 && sidebar.classList.contains('show')) {
                sidebar.classList.remove('show');
                menuButton.setAttribute('aria-expanded', 'false');
                mainContent.style.pointerEvents = 'auto';
            }
        });
    }

    const htmlEl = document.documentElement;
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        htmlEl.setAttribute('data-theme', 'dark');
    }

    window.toggleTheme = function () {
        const currentTheme = htmlEl.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        htmlEl.setAttribute('data-theme', newTheme);
        showToast(`Switched to ${newTheme.charAt(0).toUpperCase() + newTheme.slice(1)} Mode`);
    };

    window.showToast = function (message, type = 'success', duration = 4000) {
        const container = document.getElementById('toast-container');
        if (!container) return;
        const toast = document.createElement('div');
        toast.className = 'toast ' + (type === 'success' ? 'success' : 'error');
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <span class="material-icons" aria-hidden="true">${type === 'success' ? 'check_circle' : 'error'}</span>
            <div>${message}</div>
        `;
        container.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => container.removeChild(toast), 500);
        }, duration);
        toast.addEventListener('click', () => {
            toast.style.opacity = '0';
            setTimeout(() => container.removeChild(toast), 500);
        });
    };
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal').forEach(modal => modal.hidden = true);
        }
    });
    loadOrders();
});