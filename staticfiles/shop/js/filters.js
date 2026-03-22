// filters.js - Sort and filter utilities

const FilterUtils = {
    // Sort products (for client-side sorting)
    sortProducts: (products, sortBy) => {
        const sorted = [...products];
        
        switch(sortBy) {
            case 'price-low':
                return sorted.sort((a, b) => {
                    const priceA = parseFloat(a.querySelector('.product-price')?.textContent.replace('₹', '') || 0);
                    const priceB = parseFloat(b.querySelector('.product-price')?.textContent.replace('₹', '') || 0);
                    return priceA - priceB;
                });
            case 'price-high':
                return sorted.sort((a, b) => {
                    const priceA = parseFloat(a.querySelector('.product-price')?.textContent.replace('₹', '') || 0);
                    const priceB = parseFloat(b.querySelector('.product-price')?.textContent.replace('₹', '') || 0);
                    return priceB - priceA;
                });
            case 'popular':
                return sorted.sort((a, b) => {
                    const reviewsA = parseInt(a.querySelector('.reviews')?.textContent.replace(/[()]/g, '') || 0);
                    const reviewsB = parseInt(b.querySelector('.reviews')?.textContent.replace(/[()]/g, '') || 0);
                    return reviewsB - reviewsA;
                });
            case 'rating':
                return sorted.sort((a, b) => {
                    const ratingA = parseFloat(a.querySelector('.stars')?.innerHTML.match(/fa-star/g)?.length || 0);
                    const ratingB = parseFloat(b.querySelector('.stars')?.innerHTML.match(/fa-star/g)?.length || 0);
                    return ratingB - ratingA;
                });
            default:
                return sorted;
        }
    },

    // Filter by category
    filterByCategory: (products, category) => {
        if (!category || category === 'all') return products;
        return products.filter(product => {
            const productCategory = product.dataset.category;
            return productCategory === category;
        });
    },

    // Filter fashion by type (tshirt/hoodie)
    filterFashionByType: (products, type) => {
        if (!type || type === 'all') return products;
        return products.filter(product => {
            const productType = product.dataset.category;
            return productType === type;
        });
    },

    // Search products
    searchProducts: (products, query) => {
        if (!query) return products;
        const searchTerm = query.toLowerCase().trim();
        return products.filter(product => {
            const name = product.querySelector('.product-name')?.textContent.toLowerCase() || '';
            const category = product.querySelector('.product-category')?.textContent.toLowerCase() || '';
            return name.includes(searchTerm) || category.includes(searchTerm);
        });
    },

    // Filter by price range
    filterByPriceRange: (products, min, max) => {
        return products.filter(product => {
            const price = parseFloat(product.querySelector('.product-price')?.textContent.replace('₹', '') || 0);
            return price >= min && price <= max;
        });
    },

    // Filter by rating
    filterByRating: (products, minRating) => {
        return products.filter(product => {
            const rating = parseFloat(product.querySelector('.stars')?.innerHTML.match(/fa-star/g)?.length || 0);
            return rating >= minRating;
        });
    }
};

window.FilterUtils = FilterUtils;