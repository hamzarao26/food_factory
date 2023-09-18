from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomerRegistrationForm, CustomerForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .EmailBackEnd import EmailBackEnd



def home(request):
 food = Product.objects.filter(category='FF')
 drink = Product.objects.filter(category='D')
 Shaks = Product.objects.filter(category='S')
 sweetdish = Product.objects.filter(category='SD')
 product = Product.objects.all()



 context = {
    'food': food, 
    'drink': drink, 
    'shaks': Shaks, 
    'sweetdish':sweetdish, 
    'products':product,

 }
 return render(request, 'app/home.html', context)



def customerregistration(request):
 if request.method == 'POST':
  username = request.POST.get('username')
  email = request.POST.get('email')
  password = request.POST.get('password')

  if CustomUser.objects.filter(username=username).exists():
    messages.warning(request, 'Username is already taken')

  if CustomUser.objects.filter(email=email).exists():
    messages.warning(request, 'Email is already taken')

  else:
    user = CustomUser(username=username, email=email)
    user.set_password(password)
    user.user_type=2
    user.save()

    messages.success(request, 'Congratulation..! You are registered Successfully')
  

 return render(request, 'app/customerregistration.html')



def loginuser(request):
 if request.method == 'POST':
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'),)
        if user:
            #user is authenticated
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('Dashboard')
            elif user_type == '2':
                return redirect('profile')
            
 return render(request, 'app/login.html')





@login_required
def profile(request):
 if request.method == 'POST':
  form = CustomerForm(request.POST)
  if form.is_valid():
   user = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   contact_no = form.cleaned_data['contact_no']
   state = form.cleaned_data['state']
   reg = Customer(user=user, name=name, locality=locality, city=city, contact_no=contact_no, state=state)
   reg.save()
   messages.success(request, 'Data updated Succesfully..!')
 else:
  form = CustomerForm()
 return render(request, 'app/profile.html',{'form':form, 'active': 'btn-primary'})


@login_required
def address(request):
 User = request.user
 add = Customer.objects.filter(user=User)
 return render(request, 'app/address.html', {'active': 'btn-primary', 'add':add})


def product_detail(request, id):
 user = request.user
 product = Product.objects.get(id=id)
 productdetail = ProductDetail.objects.filter(product=product)

 item_exists = False
#  if request.user.is_authenticated:
#   item_exists = Cart.objects.filter(Q(user=user) & Q(Product=productdetail))
 context = {
  'product': product, 
  'productdetail': productdetail,
  # 'item_exists': item_exists
 }
 return render(request, 'app/productdetail.html', context)


def products(request, data=None):
 if data == None:
  products = Product.objects.all()
 return render(request, 'app/products.html', {'products':products})

@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 size = request.GET.get('prod_size')
 product = Product.objects.get(id=product_id)
 productdetial = ProductDetail.objects.get(product=product, size=size)
 cart = Cart(user=user, Product=productdetial)
 cart.save()
 return redirect('/cart')
 

@login_required
def showcart(request):
 user = request.user
 carts = Cart.objects.filter(user=user)
 base_amount = 0.00
 shipping_tex = 50.00
 total_amount = 0.00
 cart_product = {p for p in Cart.objects.all() if p.user==user}
 if cart_product:
  for cart in cart_product:
   tempamount = (cart.quantity * cart.Product.price)
   base_amount += tempamount
   totalamount = base_amount + shipping_tex
  return render(request, 'app/addtocart.html', {'carts': carts, 'totalamount': totalamount, 'tempamount': tempamount, 'base_amount': base_amount})
 else: 
    return render(request, 'app/emptycart.html')
 

@login_required
def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 carts = Cart.objects.filter(user=user)
 base_amount = 0.00
 shipping_tex = 70.00
 total_amount = 0.00
 cart_product = {p for p in Cart.objects.all() if p.user==user}
 if cart_product:
  for cart in cart_product:
   tempamount = (cart.quantity * cart.Product.price)
   base_amount += tempamount
   totalamount = base_amount + shipping_tex
  return render(request, 'app/checkout.html', {'add':add ,'carts':carts, 'totalamount':totalamount, 'tempamount':tempamount})
 else: 
  return render(request, 'app/emptycart.html')
 

@login_required
def payment_done(request):
 user = request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 cart = Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user, Customer=customer, product=c.Product, quantity=c.quantity).save()
  # OrderPlaced(user=user, Customer=customer, product=c.Product, quantity=c.quantity).save()
  c.delete()

 return redirect('orders')


@login_required
def orders(request):
 user= request.user
 order = OrderPlaced.objects.filter(user=user)
 return render(request, 'app/orders.html', {'order':order})


def RemoveItem(request, id):
  cart = Cart.objects.get(Product__id=id)
  cart.delete()
  return redirect('showcart')

def about(request):
 return render(request,'app/about.html')


def logoutuser(request):
  logout(request)
  return redirect('/')