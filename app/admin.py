from django.contrib import admin
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced,
    rej
)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'fee', 'discounted_price', 'description', 'school', 'category', 'lawyer_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status']

@admin.register(rej)
class RejAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'number')