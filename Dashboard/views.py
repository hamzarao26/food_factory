from django.shortcuts import render, redirect
from app.models import *
from django.contrib.auth.models import User
from app.forms import *
from django.contrib import messages

# Create your views here.


def Dashboard(request):

    return render(request, 'Dashboard/index.html' )

def CustomerList(request):
    customer = Customer.objects.all()

    context = {
        'customer': customer,
    }
    return render(request, 'Dashboard/customer.html', context)


def addproduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            discription = form.cleaned_data['discription']
            category = form.cleaned_data['category']
            product_img = form.cleaned_data['product_img']

            product = Product(title=title, discription=discription, category=category, product_img=product_img)
            product.save()
            messages.success(request,'Product Add Successfully')
            form = ProductForm()

    else:
        form = ProductForm()
        # product = request.POST.get('product')
        # discription = request.POST.get('discription')
        # category = request.POST.get('category')
        # product_img = request.FILES.get('img')

        # product = Product(title=product, discription=discription, category=category, product_img=product_img)
        # product.save()

    context = {
        'form': form
    }
    return render(request, 'Dashboard/addproduct.html', context)


def productlist(request):
    product = Product.objects.all()

    context = {
        'product': product
    }
    return render(request, 'Dashboard/product_list.html', context)


def product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST' and request.POST.get('add_product_detail', False):
        productdetail_formset = productdetailformset(request.POST, instance=product)
        if productdetail_formset.is_valid():
            if product:
                product.save()
            for form in productdetail_formset:
                product = form.cleaned_data['product']
                size = form.cleaned_data['size']
                price = form.cleaned_data['price']
                if form.has_changed():
                    form.instance.product = product
                    form.save()
            
            productdetail_formset = productdetailformset()
    else:
        productdetail_formset = productdetailformset()

    
    context = {
        'productdetail': productdetail_formset,
        'product': product
    }
    
    return render(request, 'Dashboard/product.html', context)

def orderplaced(request):
    order = OrderPlaced.objects.all()

    context = {
        'order': order
    }
    return render(request, 'Dashboard/orderplaced.html', context)


def orderdetail(request, id):
    order = OrderPlaced.objects.get(id=id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        messages.success(request, 'Order status updated successfully.')


    context = {
        'order': order
    }
    return render(request, 'Dashboard/orderdetail.html', context)




def cart(request):
    cart = Cart.objects.all()

    context = {
        'cart': cart
    }
    return render(request, 'Dashboard/cart.html', context)