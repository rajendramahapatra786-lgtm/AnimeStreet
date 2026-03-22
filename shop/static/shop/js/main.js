// main.js - Global functions for all pages

document.addEventListener('DOMContentLoaded', function() {
    
    // Update cart count on page load
    if (typeof CartService !== 'undefined') {
        const cartCountElement = document.getElementById('cartCount');
        if (cartCountElement && window.cartCount !== undefined) {
            CartService.updateCartCount(window.cartCount);
        }
    }
    
    // Update wishlist count on page load
    if (typeof WishlistService !== 'undefined') {
        WishlistService.updateWishlistCount();
    }
    
    // Handle search from sessionStorage
    const searchQuery = sessionStorage.getItem('searchQuery');
    if (searchQuery && window.location.pathname === '/') {
        const searchInput = document.getElementById('globalSearchInput');
        if (searchInput) {
            searchInput.value = searchQuery;
        }
        
        // Filter products if on index page
        if (typeof filterProductsBySearch === 'function') {
            filterProductsBySearch(searchQuery);
        }
        
        sessionStorage.removeItem('searchQuery');
    }
    
    // Add event listeners to all wishlist buttons
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const productId = this.dataset.id;
            if (productId) {
                toggleWishlist(productId, this);
            }
        });
    });
    
    // Add event listeners to all add to cart buttons
    document.querySelectorAll('.add-to-cart-btn, .add-to-cart').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const productCard = this.closest('.product-card');
            const productId = this.dataset.id || productCard?.dataset.id;
            
            // Get selected size if exists
            let size = 'M';
            const sizeBtn = productCard?.querySelector('.size-btn.active');
            if (sizeBtn) {
                size = sizeBtn.dataset.size;
            }
            
            if (productId) {
                CartService.addToCart(productId, size);
            }
        });
    });
    
    // Handle size selector buttons
    document.querySelectorAll('.size-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const container = this.closest('.size-options');
            if (container) {
                container.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });
});

// Global toggle wishlist function
window.toggleWishlist = async function(productId, btnElement) {
    const isActive = btnElement.classList.contains('active');
    
    let success;
    if (isActive) {
        success = await WishlistService.removeFromWishlist(productId);
        if (success) {
            btnElement.classList.remove('active');
        }
    } else {
        success = await WishlistService.addToWishlist(productId);
        if (success) {
            btnElement.classList.add('active');
        }
    }
};

// Global add to cart function
window.addToCart = async function(productId, size = 'M') {
    await CartService.addToCart(productId, size);
};

// Global search filter function
window.filterProductsBySearch = function(query) {
    const productsGrid = document.getElementById('allProductsGrid');
    if (!productsGrid) return;
    
    const products = Array.from(document.querySelectorAll('.product-card'));
    const filtered = FilterUtils.searchProducts(products, query);
    
    if (filtered.length === 0) {
        productsGrid.innerHTML = '<div class="no-products">No products found for "' + query + '"</div>';
        return;
    }
    
    productsGrid.innerHTML = '';
    filtered.forEach(product => {
        productsGrid.appendChild(product.cloneNode(true));
    });
    
    // Reattach event listeners after cloning
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.id;
            if (productId) {
                toggleWishlist(productId, this);
            }
        });
    });
    
    document.querySelectorAll('.add-to-cart-btn, .add-to-cart').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productCard = this.closest('.product-card');
            const productId = this.dataset.id || productCard?.dataset.id;
            let size = 'M';
            const sizeBtn = productCard?.querySelector('.size-btn.active');
            if (sizeBtn) size = sizeBtn.dataset.size;
            if (productId) CartService.addToCart(productId, size);
        });
    });
    
    document.querySelectorAll('.size-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const container = this.closest('.size-options');
            if (container) {
                container.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });
};

// Add notification styles if not exists
if (!document.querySelector('#notification-styles')) {
    const style = document.createElement('style');
    style.id = 'notification-styles';
    style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            transform: translateX(400px);
            transition: transform 0.3s ease;
            z-index: 9999;
        }
        
        .notification.show {
            transform: translateX(0);
        }
        
        .notification.error {
            background: #dc3545;
        }
        
        .no-products {
            text-align: center;
            padding: 50px;
            color: #666;
            font-size: 1.2rem;
            grid-column: 1 / -1;
        }
        
        .loading-spinner {
            grid-column: 1 / -1;
            text-align: center;
            padding: 50px;
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid #ddd;
            border-top-color: #ff6b6b;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .wishlist-btn.active {
            background: #ff6b6b;
            color: white;
        }
    `;
    document.head.appendChild(style);
}