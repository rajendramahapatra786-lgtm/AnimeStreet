from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random


# Create your models here.


class User(AbstractUser):
    """Custom User Model"""
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('fashion', 'Fashion'),
        ('watches', 'Watches'),
        ('bags', 'Bags'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    display_name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.display_name

class Product(models.Model):
    product_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    sub_category = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.5)
    reviews = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    sizes = models.JSONField(default=list)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_total(self):
        return sum(item.get_total() for item in self.items.all())
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, default='M')
    quantity = models.PositiveIntegerField(default=1)
    
    def get_total(self):
        return self.product.price * self.quantity
    
    class Meta:
        unique_together = ['cart', 'product', 'size']

class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['wishlist', 'product']


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # 🔥 NEW FIELDS
    payment_method = models.CharField(max_length=10, default="COD")
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_screenshot = models.ImageField(upload_to='payments/', blank=True, null=True)

    payment_status = models.CharField(max_length=20, default="Pending")
    status = models.CharField(max_length=20, default="Pending")
    
    order_id = models.CharField(max_length=20, unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            while True:
                random_number = random.randint(100000, 999999)
                new_id = f"ANIME{random_number}"

                if not Order.objects.filter(order_id=new_id).exists():
                    self.order_id = new_id
                    break

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.order_id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def get_total(self):
        return self.price * self.quantity
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.user.username    

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  
