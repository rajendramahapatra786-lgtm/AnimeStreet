import os
import django
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'animestreet.settings')
django.setup()

from shop.models import Category, Product

# Get or create categories
fashion_cat, _ = Category.objects.get_or_create(
    name='fashion', 
    defaults={'display_name': 'Fashion', 'icon': 'fa-tshirt'}
)
watches_cat, _ = Category.objects.get_or_create(
    name='watches', 
    defaults={'display_name': 'Watches', 'icon': 'fa-clock'}
)
bags_cat, _ = Category.objects.get_or_create(
    name='bags', 
    defaults={'display_name': 'Bags', 'icon': 'fa-bag-shopping'}
)

print("✓ Categories created/loaded")

# All your products from products.js
products = [
    # ===== FASHION - T-SHIRTS =====
    {"product_id": 1, "name": "Demon Slayer Tanjiro Kamado T-Shirt", "price": 1299, "category": "fashion", "sub_category": "tshirt", "type": "T-Shirt", "image": "shop/images/products/t-shirt/Demon Slayer Tanjiro Kamado T-Shirt.png", "rating": 4.8, "reviews": 234, "description": "High-quality cotton t-shirt featuring Tanjiro from Demon Slayer", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": True},
    {"product_id": 2, "name": "Naruto Shippuden Sage Mode T-Shirt", "price": 1199, "category": "fashion", "sub_category": "tshirt", "type": "T-Shirt", "image": "shop/images/products/t-shirt/Naruto Shippuden Sage Mode T-Shirt.png", "rating": 4.9, "reviews": 567, "description": "Naruto Uzumaki in Sage Mode design", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": True},
    {"product_id": 3, "name": "One Piece Luffy Gear 5 T-Shirt", "price": 1499, "category": "fashion", "sub_category": "tshirt", "type": "T-Shirt", "image": "shop/images/products/t-shirt/One Piece Luffy Gear 5 T-Shirt.png", "rating": 5.0, "reviews": 123, "description": "Celebrate Gear 5 with this exclusive design", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": True},
    {"product_id": 4, "name": "Jujutsu Kaisen Gojo Satoru T-Shirt", "price": 1399, "category": "fashion", "sub_category": "tshirt", "type": "T-Shirt", "image": "shop/images/products/t-shirt/Jujutsu Kaisen Gojo Satoru T-Shirt.png", "rating": 4.7, "reviews": 345, "description": "Premium t-shirt with Gojo's iconic look", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": False},
    {"product_id": 5, "name": "Attack on Titan Eren Yeager T-Shirt", "price": 1299, "category": "fashion", "sub_category": "tshirt", "type": "T-Shirt", "image": "shop/images/products/t-shirt/Attack on Titan Eren Yeager T-Shirt.png", "rating": 4.8, "reviews": 189, "description": "Survey Corps design with Eren", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": False},
    {"product_id": 6, "name": "Dragon Ball Z Goku Ultra Instinct T-Shirt", "price": 1399, "category": "fashion", "sub_category": "tshirt", "type": "T-Shirt", "image": "shop/images/products/t-shirt/Dragon Ball Z Goku Ultra Instinct T-Shirt.png", "rating": 4.9, "reviews": 456, "description": "Goku in Ultra Instinct form", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": True},
    {"product_id": 21, "name": "Blue Lock Isagi Yoichi T-Shirt", "price": 1399, "category": "fashion", "sub_category": "tshirt", "type": "T-Shirt", "image": "shop/images/products/t-shirt/Blue Lock Isagi Yoichi T-Shirt.png", "rating": 4.8, "reviews": 120, "description": "Striker ego design featuring Isagi Yoichi", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": True},
    {"product_id": 22, "name": "Black Clover Asta Anti Magic T-Shirt", "price": 1499, "category": "fashion", "sub_category": "tshirt", "type": "T-Shirt", "image": "shop/images/products/t-shirt/Black Clover Asta Anti Magic T-Shirt.png", "rating": 4.9, "reviews": 210, "description": "Asta with anti-magic sword design", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": True},
    {"product_id": 23, "name": "Solo Leveling Sung Jin-Woo Shadow T-Shirt", "price": 1599, "category": "fashion", "sub_category": "tshirt", "type": "T-Shirt", "image": "shop/images/products/t-shirt/Solo Leveling Sung Jin-Woo Shadow T-Shirt.png", "rating": 5.0, "reviews": 300, "description": "Shadow Monarch Jin-Woo design", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": True},
    {"product_id": 24, "name": "Bleach Ichigo Kurosaki Bankai T-Shirt", "price": 1399, "category": "fashion", "sub_category": "tshirt", "type": "T-Shirt", "image": "shop/images/products/t-shirt/Bleach Ichigo Kurosaki Bankai T-Shirt.png", "rating": 4.8, "reviews": 180, "description": "Ichigo Bankai form design", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": True},
    
    # ===== FASHION - HOODIES =====
    {"product_id": 7, "name": "Demon Slayer Akaza Hoodie", "price": 2499, "category": "fashion", "sub_category": "hoodie", "type": "Hoodie", "image": "shop/images/products/hoodies/Demon Slayer Akaza Hoodie.png", "rating": 4.8, "reviews": 278, "description": "Premium hoodie featuring Akaza from Demon Slayer", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": True},
    {"product_id": 8, "name": "Naruto Akatsuki Cloud Hoodie", "price": 2399, "category": "fashion", "sub_category": "hoodie", "type": "Hoodie", "image": "shop/images/products/hoodies/Naruto Akatsuki Cloud Hoodie.png", "rating": 4.8, "reviews": 456, "description": "Akatsuki cloud design hoodie", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": False},
    {"product_id": 9, "name": "Attack on Titan Scout Regiment Hoodie", "price": 2599, "category": "fashion", "sub_category": "hoodie", "type": "Hoodie", "image": "shop/images/products/hoodies/Attack on Titan Scout Regiment Hoodie.png", "rating": 4.9, "reviews": 189, "description": "Wings of Freedom design", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": True},
    {"product_id": 10, "name": "Jujutsu Kaisen Sukuna Hoodie", "price": 2699, "category": "fashion", "sub_category": "hoodie", "type": "Hoodie", "image": "shop/images/products/hoodies/Jujutsu Kaisen Sukuna Hoodie.png", "rating": 4.7, "reviews": 234, "description": "King of Curses design", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": False},
    {"product_id": 11, "name": "One Piece Straw Hat Pirates Hoodie", "price": 2499, "category": "fashion", "sub_category": "hoodie", "type": "Hoodie", "image": "shop/images/products/hoodies/One Piece Straw Hat Pirates Hoodie.png", "rating": 4.9, "reviews": 345, "description": "Straw Hat Jolly Roger design", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": True},
    {"product_id": 12, "name": "Dragon Ball Z Super Saiyan Hoodie", "price": 2799, "category": "fashion", "sub_category": "hoodie", "type": "Hoodie", "image": "shop/images/products/hoodies/Dragon Ball Z Super Saiyan Hoodie.png", "rating": 4.8, "reviews": 567, "description": "Super Saiyan transformation design", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": True},
    {"product_id": 25, "name": "Blue Lock Ego Striker Hoodie", "price": 2599, "category": "fashion", "sub_category": "hoodie", "type": "Hoodie", "image": "shop/images/products/hoodies/Blue Lock Ego Striker Hoodie.png", "rating": 4.7, "reviews": 90, "description": "Blue Lock striker themed hoodie", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": False},
    {"product_id": 26, "name": "Black Clover Black Bulls Hoodie", "price": 2699, "category": "fashion", "sub_category": "hoodie", "type": "Hoodie", "image": "shop/images/products/hoodies/Black Clover Black Bulls Hoodie.png", "rating": 4.9, "reviews": 140, "description": "Black Bulls squad hoodie", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": True},
    {"product_id": 27, "name": "Solo Leveling Shadow Army Hoodie", "price": 2799, "category": "fashion", "sub_category": "hoodie", "type": "Hoodie", "image": "shop/images/products/hoodies/Solo Leveling Shadow Army Hoodie.png", "rating": 5.0, "reviews": 200, "description": "Shadow army aesthetic hoodie", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": True},
    {"product_id": 28, "name": "Bleach Soul Reaper Hoodie", "price": 2599, "category": "fashion", "sub_category": "hoodie", "type": "Hoodie", "image": "shop/images/products/hoodies/Bleach Soul Reaper Hoodie.png", "rating": 4.8, "reviews": 160, "description": "Soul Reaper uniform style hoodie", "sizes": ["S", "M", "L", "XL"], "in_stock": True, "featured": False},
    
    # ===== WATCHES =====
    {"product_id": 13, "name": "Dragon Ball Z Chronograph Watch", "price": 3499, "category": "watches", "sub_category": "", "type": "Watch", "image": "shop/images/watches/Dragon Ball Z Chronograph Watch.png", "rating": 4.6, "reviews": 89, "description": "Official Dragon Ball Z chronograph watch", "sizes": [], "in_stock": True, "featured": True},
    {"product_id": 14, "name": "Naruto Akatsuki Cloud Watch", "price": 2999, "category": "watches", "sub_category": "", "type": "Watch", "image": "shop/images/watches/Naruto Akatsuki Cloud Watch.png", "rating": 4.7, "reviews": 145, "description": "Akatsuki cloud design analog watch", "sizes": [], "in_stock": True, "featured": True},
    {"product_id": 15, "name": "One Piece Pirate King Watch", "price": 3999, "category": "watches", "sub_category": "", "type": "Watch", "image": "shop/images/watches/One Piece Pirate King Watch.png", "rating": 4.8, "reviews": 67, "description": "Limited edition Pirate King watch", "sizes": [], "in_stock": True, "featured": False},
    {"product_id": 16, "name": "Demon Slayer Clockwork Watch", "price": 3299, "category": "watches", "sub_category": "", "type": "Watch", "image": "shop/images/watches/Demon Slayer Clockwork Watch.png", "rating": 4.5, "reviews": 34, "description": "Demon Slayer themed mechanical watch", "sizes": [], "in_stock": True, "featured": False},
    {"product_id": 29, "name": "Blue Lock Egoist Striker Watch", "price": 3499, "category": "watches", "sub_category": "", "type": "Watch", "image": "shop/images/watches/Blue Lock Egoist Striker Watch.png", "rating": 4.7, "reviews": 110, "description": "Blue Lock striker ego themed watch", "sizes": [], "in_stock": True, "featured": True},
    {"product_id": 30, "name": "Black Clover Magic Knight Watch", "price": 3299, "category": "watches", "sub_category": "", "type": "Watch", "image": "shop/images/watches/Black Clover Magic Knight Watch.png", "rating": 4.8, "reviews": 150, "description": "Magic Knight squad inspired watch", "sizes": [], "in_stock": True, "featured": True},
    {"product_id": 31, "name": "Solo Leveling Shadow Monarch Watch", "price": 3799, "category": "watches", "sub_category": "", "type": "Watch", "image": "shop/images/watches/Solo Leveling Shadow Monarch Watch.png", "rating": 5.0, "reviews": 200, "description": "Shadow Monarch premium watch design", "sizes": [], "in_stock": True, "featured": True},
    {"product_id": 32, "name": "Bleach Soul Reaper Bankai Watch", "price": 3599, "category": "watches", "sub_category": "", "type": "Watch", "image": "shop/images/watches/Bleach Soul Reaper Bankai Watch.png", "rating": 4.9, "reviews": 175, "description": "Bankai inspired luxury anime watch", "sizes": [], "in_stock": True, "featured": False},
    
    # ===== BAGS =====
    {"product_id": 17, "name": "Pikachu Electric Backpack", "price": 1899, "category": "bags", "sub_category": "", "type": "Bag", "image": "shop/images/bags/Pikachu Electric Backpack.jpg", "rating": 4.8, "reviews": 234, "description": "Pikachu face backpack with electric details", "sizes": [], "in_stock": True, "featured": True},
    {"product_id": 18, "name": "Naruto Ninja Messenger Bag", "price": 1599, "category": "bags", "sub_category": "", "type": "Bag", "image": "shop/images/bags/Naruto Ninja Messenger Bag.png", "rating": 4.7, "reviews": 178, "description": "Hidden Leaf Village messenger bag", "sizes": [], "in_stock": True, "featured": True},
    {"product_id": 19, "name": "Attack on Titan Survey Corps Backpack", "price": 2199, "category": "bags", "sub_category": "", "type": "Bag", "image": "shop/images/bags/Attack on Titan Survey Corps Backpack.png", "rating": 4.9, "reviews": 145, "description": "Survey Corps emblem backpack", "sizes": [], "in_stock": True, "featured": False},
    {"product_id": 20, "name": "Demon Slayer Kimetsu Bag", "price": 1799, "category": "bags", "sub_category": "", "type": "Bag", "image": "shop/images/bags/Demon Slayer Kimetsu Bag.png", "rating": 4.6, "reviews": 89, "description": "Demon Slayer pattern backpack", "sizes": [], "in_stock": True, "featured": True},
    {"product_id": 33, "name": "Blue Lock Ego Striker Backpack", "price": 1999, "category": "bags", "sub_category": "", "type": "Bag", "image": "shop/images/bags/Blue Lock Ego Striker Backpack.png", "rating": 4.7, "reviews": 120, "description": "Blue Lock striker themed backpack", "sizes": [], "in_stock": True, "featured": True},
    {"product_id": 34, "name": "Black Clover Black Bulls Backpack", "price": 1899, "category": "bags", "sub_category": "", "type": "Bag", "image": "shop/images/bags/Black Clover Black Bulls Backpack.png", "rating": 4.8, "reviews": 150, "description": "Black Bulls squad logo backpack", "sizes": [], "in_stock": True, "featured": True},
    {"product_id": 35, "name": "Solo Leveling Shadow Army Backpack", "price": 2199, "category": "bags", "sub_category": "", "type": "Bag", "image": "shop/images/bags/Solo Leveling Shadow Army Backpack.png", "rating": 5.0, "reviews": 180, "description": "Shadow army aesthetic backpack", "sizes": [], "in_stock": True, "featured": True},
    {"product_id": 36, "name": "Bleach Soul Reaper Backpack", "price": 1999, "category": "bags", "sub_category": "", "type": "Bag", "image": "shop/images/bags/Bleach Soul Reaper Backpack.png", "rating": 4.9, "reviews": 140, "description": "Soul Reaper uniform themed backpack", "sizes": [], "in_stock": True, "featured": False},
]

# Import products
count = 0
for p in products:
    # Get category
    if p['category'] == 'fashion':
        cat = fashion_cat
    elif p['category'] == 'watches':
        cat = watches_cat
    else:
        cat = bags_cat
    
    # Check if product already exists
    if not Product.objects.filter(product_id=p['product_id']).exists():
        Product.objects.create(
            product_id=p['product_id'],
            name=p['name'],
            price=p['price'],
            category=cat,
            sub_category=p.get('sub_category', ''),
            type=p.get('type', ''),
            image=p['image'],
            rating=p['rating'],
            reviews=p['reviews'],
            description=p['description'],
            sizes=p.get('sizes', []),
            in_stock=p.get('in_stock', True),
            featured=p.get('featured', False)
        )
        count += 1
        print(f"✓ Added: {p['name']}")
    else:
        print(f"○ Skipped (exists): {p['name']}")

print(f"\n✅ Successfully imported {count} new products!")
print(f"📊 Total products in database: {Product.objects.count()}")