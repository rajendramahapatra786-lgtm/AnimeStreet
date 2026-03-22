from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json

from .models import Category, Product, Cart, CartItem, Wishlist, WishlistItem, Order, OrderItem
from .forms import SignupForm
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
    """User registration page"""
    if request.user.is_authenticated:
        return redirect('shop:index')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to AnimeStreet!')
            return redirect('shop:index')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = SignupForm()
    
    return render(request, 'shop/signup.html', {'form': form})

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
    orders = Order.objects.filter(user=request.user)
    
    cart_items = cart.items.select_related('product').all()
    wishlist_items = wishlist.items.select_related('product').all()
    
    cart_total = cart.get_total()
    total_orders = orders.count()
    total_spent = sum(order.total_amount for order in orders)
    
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
    """Shopping cart page"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    subtotal = cart.get_total()
    tax = subtotal * 0.18
    total = subtotal + tax
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
    }
    return render(request, 'shop/cart.html', context)

@login_required
def wishlist(request):
    """Wishlist page"""
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_items = wishlist.items.select_related('product').all()
    context = {'wishlist_items': wishlist_items}
    return render(request, 'shop/wishlist.html', context)

@login_required
def checkout(request):
    """Checkout page"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('shop:cart')
    
    subtotal = cart.get_total()
    tax = subtotal * 0.18
    total = subtotal + tax
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
    }
    return render(request, 'shop/checkout.html', context)

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
        tax = subtotal * 0.18
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
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.select_related('product').all()
        
        if not cart_items.exists():
            return JsonResponse({'success': False, 'message': 'Cart is empty'})
        
        subtotal = cart.get_total()
        tax = subtotal * 0.18
        total = subtotal + tax
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            status='processing'
        )
        
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
            'order_id': str(order.order_id)
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})