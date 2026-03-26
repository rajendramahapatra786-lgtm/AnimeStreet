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

                // 🔥 INSTANT COUNT
                WishlistService.incrementWishlistCount();

                // ✅ sync + UI state
                await WishlistService.updateWishlistCount();
                await WishlistService.loadWishlistState();

                return true;
            } else {
                Helpers.showNotification(data.message, 'error');
                return false;
            }
        } catch (error) {
            console.error('Error:', error);
            Helpers.showNotification('Please log in to add items to your wishlist', 'error');
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

                // 🔥 DECREASE COUNT
                WishlistService.decrementWishlistCount();

                // ✅ sync + UI state
                await WishlistService.updateWishlistCount();
                await WishlistService.loadWishlistState();

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

    // 🔥 Load state (active heart)
    loadWishlistState: async () => {
        try {
            const response = await fetch('/api/wishlist-ids/');
            const data = await response.json();

            const ids = data.ids || [];

            document.querySelectorAll('.wishlist-btn').forEach(btn => {
                const productId = parseInt(btn.dataset.id);

                if (ids.includes(productId)) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });

        } catch (error) {
            console.error('Wishlist load error:', error);
        }
    },

    // 🔥 Update count from backend
    updateWishlistCount: async () => {
        try {
            const response = await fetch('/api/wishlist-count/');
            const data = await response.json();

            const count = data.count || 0;

            document.querySelectorAll('#wishlistCount').forEach(badge => {
                badge.textContent = count;
                badge.style.display = count > 0 ? 'inline-block' : 'none';
            });

        } catch (error) {
            console.error('Wishlist count error:', error);
        }
    },

    // 🔥 Instant increase
    incrementWishlistCount: () => {
        document.querySelectorAll('#wishlistCount').forEach(badge => {
            let count = parseInt(badge.textContent) || 0;
            count += 1;
            badge.textContent = count;
            badge.style.display = 'inline-block';
        });
    },

    // 🔥 Instant decrease
    decrementWishlistCount: () => {
        document.querySelectorAll('#wishlistCount').forEach(badge => {
            let count = parseInt(badge.textContent) || 0;
            count = Math.max(0, count - 1);
            badge.textContent = count;
            badge.style.display = count > 0 ? 'inline-block' : 'none';
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