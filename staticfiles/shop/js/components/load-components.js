// load-components.js - Loads navbar and footer (Now using Django includes, so this file is optional)
// Since we're using Django template includes, this file is not needed for loading components
// But keep it for any component-specific JS

// load-components.js - Component initialization
// Since Django uses template includes, this file is for any additional component JS

document.addEventListener('DOMContentLoaded', function() {
    // Highlight current page in navbar
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '/' && href === '/')) {
            link.classList.add('active');
        }
    });
    
    // Setup global search
    const searchInput = document.getElementById('globalSearchInput');
    const searchBtn = document.getElementById('globalSearchBtn');
    
    if (searchInput && searchBtn) {
        const performSearch = () => {
            const query = searchInput.value.trim();
            if (query) {
                sessionStorage.setItem('searchQuery', query);
                window.location.href = '/';
            }
        };
        
        searchBtn.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
});