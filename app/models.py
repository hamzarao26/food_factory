from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from tinymce.models import HTMLField
from django.contrib.auth.models import AbstractUser 


# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE = (
        (1, 'Admin'),
        (2, 'User')
    )
    user_type = models.CharField(choices=USER_TYPE, max_length=25, default=1)


STATE_CHOICES = (
    ('Punjab', 'Punjab'),
    ('Sindh', 'Sindh'),
    ('KPK', 'KPK'),
    ('Blochistan', 'blochistan'),
    ('Kashmir', 'Kashimir')
)

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    locality = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    contact_no = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=20)

    def __str__(self):
        return str(self.id)
    

CATEGORY_CHOICES = (
    ('FF', 'Fast Food'),
    ('D', 'Drink'),
    ('S', 'Shaks'),
    ('SD', 'SWeet Dish'),
)



class Product(models.Model):
    title = models.CharField(max_length=50)
    discription = HTMLField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    product_img = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)


PRODUCT_SIZE = (
    ('Small', 'Small'),
    ('Medium', 'Medium'),
    ('Large', 'Large'),
    ('Extra Large', 'Extra Large'),
)

class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(choices=PRODUCT_SIZE, max_length=25)
    price = models.FloatField()

    def __str__(self):
        return self.product.title
    



class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    Product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    

STATUS_CHOICE = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the Way', 'On the way'),
    ('Delivered','Delivered'),
    ('Cancel', 'Cancel')
)

class OrderPlaced(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    order_data = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(choices=STATUS_CHOICE, default='Pending', max_length=50)

