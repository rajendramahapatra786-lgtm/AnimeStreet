// wishlist.js - Wishlist functionality with Django API

const WishlistService = {
    // Add to wishlist
    addToWishlist: async (productId) => {
        try {
            const response = await fetch('/api/add-to-wishlist/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': Helpers.getCSRFToken()
                },
                body: JSON.stringify({
                    product_id: parseInt(productId)
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                Helpers.showNotification(data.message, 'success');
                WishlistService.updateWishlistCount();
                return true;
            } else {
                Helpers.showNotification(data.message, 'error');
                return false;
            }
        } catch (error) {
            console.error('Error:', error);
            Helpers.showNotification('Error adding to wishlist', 'error');
            return false;
        }
    },

    // Remove from wishlist
    removeFromWishlist: async (productId) => {
        try {
            const response = await fetch('/api/remove-from-wishlist/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': Helpers.getCSRFToken()
                },
                body: JSON.stringify({
                    product_id: parseInt(productId)
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                Helpers.showNotification(data.message, 'success');
                WishlistService.updateWishlistCount();
                return true;
            } else {
                Helpers.showNotification(data.message, 'error');
                return false;
            }
        } catch (error) {
            console.error('Error:', error);
            Helpers.showNotification('Error removing from wishlist', 'error');
            return false;
        }
    },

    // Check if in wishlist (from button active class)
    isInWishlist: (productId) => {
        const btn = document.querySelector(`.wishlist-btn[data-id="${productId}"]`);
        return btn ? btn.classList.contains('active') : false;
    },

    // Update wishlist count display
    updateWishlistCount: () => {
        const wishlistItems = document.querySelectorAll('.wishlist-item');
        const count = wishlistItems.length;
        
        const wishlistBadges = document.querySelectorAll('#wishlistCount');
        wishlistBadges.forEach(badge => {
            if (badge) {
                badge.textContent = count;
                if (count > 0) {
                    badge.style.display = 'inline-block';
                } else {
                    badge.style.display = 'none';
                }
            }
        });
    },

    // Move to cart
    moveToCart: async (productId, size = 'M') => {
        const added = await CartService.addToCart(productId, size);
        if (added) {
            await WishlistService.removeFromWishlist(productId);
            return true;
        }
        return false;
    }
};

window.WishlistService = WishlistService;