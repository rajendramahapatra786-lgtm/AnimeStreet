from .models import Cart

def cart_count(request):
    """Add cart count to all templates"""
    if request.user.is_authenticated:
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            count = cart.get_total_items()
        except:
            count = 0
    else:
        count = 0
    return {'cart_count': count}