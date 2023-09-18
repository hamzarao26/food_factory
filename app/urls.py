from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home),
    path('product-detail/<int:id>/', views.product_detail, name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.showcart, name='showcart'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('products/<str:data>', views.products, name='productsdetail'),
    path('products/', views.products, name='products'),
    path('remove/<int:id>/', views.RemoveItem, name='RemoveItem'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('registration/', views.customerregistration, name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
