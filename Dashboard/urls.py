from django.urls import path
from .views import *

urlpatterns = [
    path('Dashboard/', Dashboard, name='Dashboard'),
    path('Customer/', CustomerList, name='Customer'),
    path('add-product/', addproduct, name='add-product'),
    path('product-list/', productlist, name='Product-list'),
    path('product/<int:id>/', product, name='Product'),
    path('order-placed/', orderplaced, name='orderplaced'),
    path('order-detail/<int:id>/', orderdetail, name='orderdetail'),
    path('CartList/', cart, name='CartList')
]
