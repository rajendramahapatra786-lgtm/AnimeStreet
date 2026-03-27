// main.js (FINAL WORKING)

document.addEventListener("DOMContentLoaded", async () => {

    console.log("MAIN JS RUNNING 🔥");

    // ✅ Wishlist count
    if (window.WishlistService) {
        try {
            const res = await fetch('/api/wishlist-count/');
            const data = await res.json();

            document.querySelectorAll('#wishlistCount').forEach(badge => {
                badge.textContent = data.count;
                badge.style.display = data.count > 0 ? 'inline-block' : 'none';
            });

            await WishlistService.loadWishlistState();

        } catch (err) {
            console.error("Wishlist error:", err);
        }
    }

    // ✅ Cart count
    if (window.CartService) {
        try {
            const res = await fetch('/api/cart-ids/');
            const data = await res.json();

            const count = data.ids ? data.ids.length : 0;

            document.querySelectorAll('#cartCount').forEach(badge => {
                badge.textContent = count;
                badge.style.display = count > 0 ? 'inline-block' : 'none';
            });

            await CartService.loadCartState();

        } catch (err) {
            console.error("Cart error:", err);
        }
    }

});
    // 🔥 WISHLIST TOGGLE FUNCTION

    window.toggleWishlist = async function (productId, btnElement) {
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

        // ✅ ALWAYS UPDATE COUNT
        try {
            const res = await fetch('/api/wishlist-count/');
            const data = await res.json();

            document.querySelectorAll('#wishlistCount').forEach(badge => {
                badge.textContent = data.count;
                badge.style.display = data.count > 0 ? 'inline-block' : 'none';
            });

        } catch (err) {
            console.error("Wishlist count update error:", err);
        }
    };
    document.addEventListener('click', function (e) {

        const wishlistBtn = e.target.closest('.wishlist-btn');
        if (wishlistBtn) {
            e.preventDefault();
            e.stopPropagation();

            const productId = wishlistBtn.dataset.id;
            if (productId) toggleWishlist(productId, wishlistBtn);
        }

        const cartBtn = e.target.closest('.add-to-cart-btn, .add-to-cart');
        if (cartBtn) {
            e.preventDefault();
            e.stopPropagation();

            const productCard = cartBtn.closest('.product-card');
            const productId = cartBtn.dataset.id || productCard?.dataset.id;

            let size = 'M';
            const sizeBtn = productCard?.querySelector('.size-btn.active');
            if (sizeBtn) size = sizeBtn.dataset.size;

            if (productId) {
                CartService.addToCart(productId, size);
            }
        }

    });