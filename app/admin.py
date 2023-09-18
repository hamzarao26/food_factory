from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from . models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserModel(UserAdmin):
    
    list_display = ['username', 'user_type']


admin.site.register(CustomUser, UserModel)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'contact_no', 'state']

admin.site.register(Customer, CustomerAdmin)





class ProductDetailInline(admin.StackedInline):
    model = ProductDetail
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductDetailInline]
    list_display = ['id', 'title', 'discription', 'category', 'product_img']
admin.site.register(Product, ProductAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'Product', 'quantity']

admin.site.register(Cart, CartAdmin)


class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'Customer', 'customer_info', 'product', 'product_info', 'order_data', 'status']

    def customer_info(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.Customer.id])
        return format_html('<a href="{}">{}</a>', link, obj.Customer.name)
    
    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', link, obj.product.product.title)


admin.site.register(OrderPlaced, OrderPlacedAdmin)