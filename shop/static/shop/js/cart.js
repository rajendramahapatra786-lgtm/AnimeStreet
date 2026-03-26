// cart.js - Shopping cart functionality with Django API

const CartService = {

    // Add item to cart via API
    addToCart: async (productId, size = 'M', quantity = 1) => {
        try {
            const response = await fetch('/api/add-to-cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': Helpers.getCSRFToken()
                },
                body: JSON.stringify({
                    product_id: parseInt(productId),
                    size: size,
                    quantity: quantity
                })
            });

            const data = await response.json();

            if (data.success) {
                Helpers.showNotification(data.message, 'success');

                // 🔥 INSTANT COUNT
                CartService.incrementCartCount();

                // ✅ backend sync
                CartService.updateCartCount(data.cart_count);
                CartService.loadCartState();

                return true;
            } else {
                Helpers.showNotification(data.message, 'error');
                return false;
            }
        } catch (error) {
            console.error('Error:', error);
            Helpers.showNotification('Please log in to add items to your cart', 'error');
            return false;
        }
    },

    // Remove from cart
    removeFromCart: async (productId, size = 'M') => {
        try {
            const response = await fetch('/api/remove-from-cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': Helpers.getCSRFToken()
                },
                body: JSON.stringify({
                    product_id: parseInt(productId),
                    size: size
                })
            });

            const data = await response.json();

            if (data.success) {
                Helpers.showNotification(data.message, 'success');

                // 🔥 DECREASE COUNT
                CartService.decrementCartCount();

                // ✅ backend sync
                CartService.updateCartCount(data.cart_count);
                CartService.loadCartState();

                return true;
            } else {
                Helpers.showNotification(data.message, 'error');
                return false;
            }
        } catch (error) {
            console.error('Error:', error);
            Helpers.showNotification('Error removing from cart', 'error');
            return false;
        }
    },

    // 🔥 Instant increase
    incrementCartCount: () => {
        document.querySelectorAll('#cartCount').forEach(badge => {
            let count = parseInt(badge.textContent) || 0;
            count += 1;
            badge.textContent = count;
            badge.style.display = 'inline-block';
        });
    },

    // 🔥 Instant decrease
    decrementCartCount: () => {
        document.querySelectorAll('#cartCount').forEach(badge => {
            let count = parseInt(badge.textContent) || 0;
            count = Math.max(0, count - 1);
            badge.textContent = count;
            badge.style.display = count > 0 ? 'inline-block' : 'none';
        });
    },

    // Update cart count display (backend)
    updateCartCount: (count) => {
        const cartBadges = document.querySelectorAll('#cartCount');
        cartBadges.forEach(badge => {
            if (badge) {
                badge.textContent = count || 0;
                badge.style.display = count > 0 ? 'inline-block' : 'none';
            }
        });
    },

    // Load cart state (active button)
    loadCartState: async () => {
        try {
            const response = await fetch('/api/cart-ids/');
            const data = await response.json();

            const ids = data.ids || [];

            document.querySelectorAll('.add-to-cart-btn, .add-to-cart').forEach(btn => {
                const productId = parseInt(btn.dataset.id);

                if (ids.includes(productId)) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });

        } catch (error) {
            console.error('Cart load error:', error);
        }
    },

    // Get cart total
    getCartTotal: () => {
        const totalElement = document.getElementById('cartTotal');
        if (totalElement) {
            return parseFloat(totalElement.textContent.replace('₹', ''));
        }
        return 0;
    },

    // Proceed to checkout
    proceedToCheckout: () => {
        window.location.href = '/checkout/';
    }

};

window.CartService = CartService;