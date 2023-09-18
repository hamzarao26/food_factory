from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import inlineformset_factory
from tinymce.widgets import TinyMCE


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(required=True, label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, label='User Name', widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        label = {'email': 'Email'}


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'contact_no', 'state']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'locality': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'contact_no': forms.NumberInput(attrs={'class':'form-control'}),
            'state': forms.Select(attrs={'class':'form-control'}),                       
        }


class ProductForm(forms.ModelForm):
    discription = forms.CharField(widget=TinyMCE(attrs={'class':'form-control', 'cols': 80, 'rows': 10}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Product
        fields = ("title", "discription", "category", "product_img")

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'product_img': forms.FileInput(attrs={'class': 'form-control'})
        }



class ProductDetailForm(forms.ModelForm): 
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    size = forms.ChoiceField(choices=PRODUCT_SIZE, widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = ProductDetail
        fields = ['product', 'size', 'price']

        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Write Degree Name'}),
        }

productdetailformset = inlineformset_factory(Product, ProductDetail, form=ProductDetailForm, extra=1)