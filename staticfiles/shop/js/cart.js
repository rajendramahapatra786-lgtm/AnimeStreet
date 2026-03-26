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
                CartService.updateCartCount(data.cart_count);
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
                CartService.updateCartCount(data.cart_count);
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

    // Update quantity
    updateQuantity: async (productId, size, quantity) => {
        try {
            const response = await fetch('/api/update-cart/', {
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
                CartService.updateCartCount(data.cart_count);
                return data;
            } else {
                Helpers.showNotification(data.message, 'error');
                return null;
            }
        } catch (error) {
            console.error('Error:', error);
            Helpers.showNotification('Error updating cart', 'error');
            return null;
        }
    },

    // Update cart count display
    updateCartCount: (count) => {
        const cartBadges = document.querySelectorAll('#cartCount');
        cartBadges.forEach(badge => {
            if (badge) {
                badge.textContent = count || 0;
                if (count > 0) {
                    badge.style.display = 'inline-block';
                } else {
                    badge.style.display = 'none';
                }
            }
        });
    },

    // Get cart total from page or API
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