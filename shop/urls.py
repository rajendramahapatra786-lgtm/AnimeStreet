from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('fashion/', views.fashion, name='fashion'),
    path('bags/', views.bags, name='bags'),
    path('watches/', views.watches, name='watches'),
    
    # User pages
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Cart & Wishlist
    path('cart/', views.cart, name='cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('checkout/', views.checkout, name='checkout'),
    
    # API endpoints
    path('api/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('api/remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('api/update-cart/', views.update_cart, name='update_cart'),
    path('api/add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('api/remove-from-wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('api/place-order/', views.place_order, name='place_order'),

    # path('api/cart-ids/', views.get_cart_ids),

    path('api/wishlist-count/', views.wishlist_count),
    path('api/wishlist-ids/', views.wishlist_ids),
    path('api/cart-ids/', views.cart_ids),

    path('verify-otp/', views.verify_signup_otp, name='verify_signup_otp'),

    path('edit-profile/', views.edit_profile, name='edit_profile'),


    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/approve/<int:id>/', views.approve_order, name='approve_order'),
    path('admin/reject/<int:id>/', views.reject_order, name='reject_order'),
]