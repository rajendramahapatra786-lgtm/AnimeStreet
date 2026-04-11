from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from decimal import Decimal 
from django.http import JsonResponse
from .models import CartItem

from .models import Category, Product, Cart, CartItem, Wishlist, WishlistItem, Order, OrderItem
from .forms import SignupForm


from django.http import JsonResponse
from .models import WishlistItem

import random
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Profile
from .models import Cart, CartItem


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order

from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    """Home page - shows featured and all products"""
    featured_products = Product.objects.filter(featured=True)[:4]
    all_products = Product.objects.all()
    categories = Category.objects.all()
    
    context = {
        'featured_products': featured_products,
        'all_products': all_products,
        'categories': categories,
    }
    return render(request, 'shop/index.html', context)

def fashion(request):
    """Fashion page with t-shirts and hoodies"""
    products = Product.objects.filter(category__name='fashion')
    tshirts = products.filter(sub_category='tshirt')
    hoodies = products.filter(sub_category='hoodie')
    
    context = {
        'products': products,
        'tshirts': tshirts,
        'hoodies': hoodies,
    }
    return render(request, 'shop/fashion.html', context)

def bags(request):
    """Bags page"""
    products = Product.objects.filter(category__name='bags')
    context = {'products': products}
    return render(request, 'shop/bags.html', context)

def watches(request):
    """Watches page"""
    products = Product.objects.filter(category__name='watches')
    context = {'products': products}
    return render(request, 'shop/watches.html', context)

# ==================== AUTHENTICATION VIEWS ====================


# def get_cart_ids(request):
#     if request.user.is_authenticated:
#         items = Cart.objects.filter(user=request.user).values_list('product_id', flat=True)
#         return JsonResponse({'ids': list(items)})
#     return JsonResponse({'ids': []})


def login_view(request):
    """User login page"""
    if request.user.is_authenticated:
        return redirect('shop:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('shop:index')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'shop/login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('shop:index')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            otp = random.randint(1000, 9999)

            # Store in session
            request.session['signup_data'] = form.cleaned_data
            request.session['otp'] = otp

            email = form.cleaned_data.get('email')

            # ✅ EMAIL CODE INSIDE HERE
            subject = "🔐 AnimeStreet OTP Verification"

            text_content = f"""
Hi 👋,

Your OTP for AnimeStreet is: {otp}

This code is valid for 5 minutes.

- AnimeStreet Team
"""

            html_content = f"""
<div style="font-family: Arial; padding: 20px; background:#f4f4f4;">
    <div style="max-width:500px; margin:auto; background:white; padding:20px; border-radius:10px; text-align:center;">
        <h2 style="color:#ff4d6d;">AnimeStreet 🔐</h2>
        <p>Your OTP code is:</p>
        <h1 style="letter-spacing:6px;">{otp}</h1>
        <p>This OTP is valid for <b>5 minutes</b>.</p>
    </div>
</div>
"""

            email_msg = EmailMultiAlternatives(
                subject,
                text_content,
                "AnimeStreet <supportanimestreet@gmail.com>",
                [email]
            )

            email_msg.attach_alternative(html_content, "text/html")
            email_msg.send()

            return redirect('shop:verify_signup_otp')

        else:
            for error in form.errors.values():
                messages.error(request, error)

    else:
        form = SignupForm()

    return render(request, 'shop/signup.html', {'form': form})


def verify_signup_otp(request):
    if request.method == "POST":
        user_otp = request.POST.get('otp')

        if str(user_otp) == str(request.session.get('otp')):

            data = request.session.get('signup_data')

            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password1']
            )

            messages.success(request, "Account created successfully 🎉")

            # Clear session
            request.session.pop('otp', None)
            request.session.pop('signup_data', None)

            return redirect('shop:login')

        else:
            messages.error(request, "Invalid OTP ❌")

    return render(request, 'shop/verify_otp.html')

def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('shop:index')

@login_required
def profile(request):
    """User profile page"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:4]    
    cart_items = cart.items.select_related('product').all()
    wishlist_items = wishlist.items.select_related('product').all()
    
    cart_total = cart.get_total()
    total_orders = orders.count()
    total_spent = sum(order.total_price for order in orders)    
    context = {
        'user': request.user,
        'cart_items': cart_items,
        'wishlist_items': wishlist_items,
        'orders': orders,
        'cart_total': cart_total,
        'total_orders': total_orders,
        'total_spent': total_spent,
    }
    return render(request, 'shop/profile.html', context)

# ==================== CART & WISHLIST VIEWS ====================

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    subtotal = cart.get_total()
    tax = subtotal * Decimal('0.18')
    total = subtotal + tax
    
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
    })

@login_required
def wishlist(request):
    """Wishlist page"""
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_items = wishlist.items.select_related('product').all()
    context = {'wishlist_items': wishlist_items}
    return render(request, 'shop/wishlist.html', context)

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    if not cart_items.exists():
        return redirect('shop:cart')
    
    subtotal = cart.get_total()
    tax = subtotal * Decimal('0.18')
    total = subtotal + tax
    
    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
    })
# ==================== API ENDPOINTS ====================

@csrf_exempt
@login_required
def add_to_cart(request):
    """API endpoint to add item to cart"""
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        size = data.get('size', 'M')
        quantity = data.get('quantity', 1)
        
        product = get_object_or_404(Product, product_id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart!',
            'cart_count': cart.get_total_items()
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
@login_required
def remove_from_cart(request):
    """API endpoint to remove item from cart"""
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        size = data.get('size', 'M')
        
        product = get_object_or_404(Product, product_id=product_id)
        cart = Cart.objects.get(user=request.user)
        
        CartItem.objects.filter(cart=cart, product=product, size=size).delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart',
            'cart_count': cart.get_total_items()
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
@login_required
def update_cart(request):
    """API endpoint to update cart item quantity"""
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        size = data.get('size', 'M')
        quantity = data.get('quantity', 1)
        
        product = get_object_or_404(Product, product_id=product_id)
        cart = Cart.objects.get(user=request.user)
        
        cart_item = CartItem.objects.get(cart=cart, product=product, size=size)
        cart_item.quantity = quantity
        cart_item.save()
        
        if quantity <= 0:
            cart_item.delete()
        
        subtotal = cart.get_total()
        tax = subtotal *  Decimal('0.18')
        total = subtotal + tax
        
        return JsonResponse({
            'success': True,
            'subtotal': float(subtotal),
            'tax': float(tax),
            'total': float(total),
            'cart_count': cart.get_total_items()
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
@login_required
def add_to_wishlist(request):
    """API endpoint to add item to wishlist"""
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        product = get_object_or_404(Product, product_id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        
        wishlist_item, created = WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            product=product
        )
        
        if created:
            return JsonResponse({
                'success': True,
                'message': f'{product.name} added to wishlist!'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Item already in wishlist'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
@login_required
def remove_from_wishlist(request):
    """API endpoint to remove item from wishlist"""
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        product = get_object_or_404(Product, product_id=product_id)
        wishlist = Wishlist.objects.get(user=request.user)
        
        WishlistItem.objects.filter(wishlist=wishlist, product=product).delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from wishlist'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
@login_required
def place_order(request):
    """API endpoint to place order"""
    if request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.select_related('product').all()
        
        if not cart_items.exists():
            return JsonResponse({'success': False, 'message': 'Cart is empty'})
        
        subtotal = cart.get_total()
        tax = subtotal * Decimal('0.18')
        total = subtotal + tax
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            status='pending'
        )
        send_order_email(order)

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                size=item.size,
                quantity=item.quantity,
                price=item.product.price
            )
        
        # Clear cart
        cart.items.all().delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Order placed successfully!',
            'order_id': order.id
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


# ✅ COUNT API
def wishlist_count(request):
    if request.user.is_authenticated:
        from .models import Wishlist, WishlistItem

        try:
            wishlist = Wishlist.objects.get(user=request.user)
            count = WishlistItem.objects.filter(wishlist=wishlist).count()
        except Wishlist.DoesNotExist:
            count = 0
    else:
        count = 0

    return JsonResponse({'count': count})

# ✅ IDS API (VERY IMPORTANT)
def wishlist_ids(request):
    if request.user.is_authenticated:
        from .models import Wishlist, WishlistItem

        try:
            wishlist = Wishlist.objects.get(user=request.user)
            ids = list(
                WishlistItem.objects.filter(wishlist=wishlist)
                .values_list('product__product_id', flat=True)
            )
        except Wishlist.DoesNotExist:
            ids = []
    else:
        ids = []

    return JsonResponse({'ids': ids})

def cart_ids(request):
    if request.user.is_authenticated:
        ids = list(
            CartItem.objects.filter(cart__user=request.user)
            .values_list('product__product_id', flat=True)
        )
    else:
        ids = []

    return JsonResponse({'ids': ids})


def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")
        profile.city = request.POST.get("city")
        profile.state = request.POST.get("state")
        profile.pincode = request.POST.get("pincode")

        profile.save()
        return redirect("shop:profile")
    return render(request, "shop/edit_profile.html", {"profile": profile})

# def checkout(request):
#     profile = request.user.profile

#     if not profile.address or not profile.pincode:
#         return redirect("edit_profile")

#     return render(request, "shop/checkout.html", {"profile": profile})

# def add_to_cart(request):
#     data = json.loads(request.body)

#     product_id = data.get('product_id')
#     size = data.get('size')

#     cart, created = Cart.objects.get_or_create(user=request.user)

#     item, created = CartItem.objects.get_or_create(
#         cart=cart,
#         product_id=product_id,
#         size=size
#     )

#     if not created:
#         item.quantity += 1
#         item.save()

#     return JsonResponse({'success': True})

# def cart(request):
#     cart, created = Cart.objects.get_or_create(user=request.user)

#     cart_items = cart.items.all()

#     return render(request, 'shop/cart.html', {
#         'cart_items': cart_items
#     })

# def checkout(request):
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_items = cart.items.all()

#     if not cart_items:
#         return redirect('shop:cart')

#     return render(request, 'shop/checkout.html', {
#         'cart_items': cart_items
#     })


@staff_member_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'shop/admin_orders.html', {'orders': orders})


@staff_member_required
def approve_order(request, id):
    order = get_object_or_404(Order, id=id)
    order.payment_status = "Paid"
    order.status = "processing"
    order.save()
    return redirect('shop:admin_orders')


@staff_member_required
def reject_order(request, id):
    order = get_object_or_404(Order, id=id)
    order.payment_status = "Rejected"
    order.status = "cancelled"
    order.save()
    return redirect('shop:admin_orders')


def send_order_email(order):
    subject = "New Order - AnimeStreet 🛒"

    message = f"""
New Order Received!

User: {order.user.username}
Amount: ₹{order.total_price}
Payment: {order.payment_method}
Txn ID: {order.transaction_id}

Approve:
http://127.0.0.1:8000/shop/admin/approve/{order.id}/

Reject:
http://127.0.0.1:8000/shop/admin/reject/{order.id}/
"""

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,   # same email
        [settings.EMAIL_HOST_USER], # send to yourself
        fail_silently=False,
    )

@login_required
def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        payment_method = request.POST.get('payment_method')

        order.payment_method = payment_method

        # ✅ UPI FLOW
        if payment_method == "UPI":
            order.transaction_id = request.POST.get('transaction_id')

            if request.FILES.get('screenshot'):
                order.payment_screenshot = request.FILES['screenshot']

            order.payment_status = "Verification"
            order.status = "pending"
            order.save()

            # 🔥 UPI → SUCCESS PAGE
            return redirect('shop:order_success', order_id=order.id)

        # ✅ COD FLOW
        elif payment_method == "COD":
            order.payment_status = "Pending"
            order.status = "processing"
            order.save()

            # 🔥 COD → PROFILE PAGE (or index)
            return redirect('shop:profile')   # OR 'shop:index'

    return render(request, 'shop/payment.html', {'order': order})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_success.html', {'order': order})

def payment_loading(request):
    return render(request, 'payment_loading.html')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/my_orders.html', {
        'orders': orders
    })


@login_required
def order_detail(request, id):
    order = Order.objects.get(id=id, user=request.user)
    return render(request, 'shop/order_detail.html', {'order': order})