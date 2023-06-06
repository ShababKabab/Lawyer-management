from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import csv
import random
from .forms import rejis
from .models import rej

class ProductView(View):
 def get(self, request):
  A = Product.objects.filter(category='A')
  B = Product.objects.filter(category='B')
  C = Product.objects.filter(category='C')
  D = Product.objects.filter(category='D')
  return render(request, 'app/home.html', {'A':A, 'B':B, 'C':C, 'D':D})

class ProductDetailView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()

  return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart})

def add_to_cart(request):
 user=request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  communication_cost = 10.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    totalamount = amount + communication_cost
   return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount})
  else:
   return render(request, 'app/emptycart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')


def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  amount = 0.0
  shipping_amount = 10.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount

  data = {
   'amount': amount,
   'totalamount': amount + shipping_amount
  }
  return JsonResponse(data)

def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html', {'order_placed':op})

def mobile(request):
 return render(request, 'app/mobile.html')

def taxCalculation(request):
 return render(request, 'app/taxCalculation.html')

class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form':form})

 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully')
   form.save()
  return render(request, 'app/customerregistration.html', {'form': form})


# class mobile(View):
#  def get(self, request, company_id):
#   company = get_object_or_404(Company, id=company_id)
#   form = TINForm()
#   return render(request, 'app/home.html', {'form': form, 'company': company})
#
#  def post(self, request, company_id):
#   company = get_object_or_404(Company, id=company_id)
#   form = TINForm(request.POST)
#   if form.is_valid():
#    tin = form.cleaned_data['tin']
#    contact_person = form.cleaned_data['contact_person']
#    phone_number = form.cleaned_data['phone_number']
#    company.tin = tin
#    company.contact_person = contact_person
#    company.phone_number = phone_number
#    company.save()
#   return render(request, 'app/home.html', {'form': form, 'company': company})

def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 10.0
 totalamount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount
  totalamount = amount + shipping_amount
 return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})

def payment_done(request):
 user = request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 cart = Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
  c.delete()
 return redirect("orders")

# @method_decorator(login_required, name='dispatch')
class ProfileView(View):
 def get(self, request):
  form = CustomerProfileForm()
  return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
   reg.save()
   messages.success(request, 'Congratulations!! Profile Updated Successfully')
  return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

def tinregistration(request):
 return render(request, 'app/tinregistration.html')

def venue_pdf(request):
 buf = io.BytesIO()
 c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
 textob = c.beginText()
 textob.setTextOrigin(inch, inch)
 textob.setFont("Helvetica", 14)

 # lines = [
 #  "This is NID"
 # ]

 venues = [p for p in Customer.objects.all() if p.user == request.user]
 lines = []
 for venue in venues:
  lines.append(venue.name)
  lines.append(venue.city)
  lines.append("NID Number:" + generate_random_number())
  break

 for line in lines:
  textob.textLine(line)

 c.drawText(textob)
 c.showPage()
 c.save()
 buf.seek(0)

 return FileResponse(buf, as_attachment=True, filename='vanue.pdf')


def generate_random_number():
 return ''.join(random.choices('0123456789', k=10))

def generate_random_numberT():
 return ''.join(random.choices('0123456789', k=5))

def showformdata(request):
 if request.method == 'POST':
  fm = rejis(request.POST)
  if fm.is_valid():
   nm = fm.cleaned_data['name']
   em = fm.cleaned_data['address']
   pw = fm.cleaned_data['number']
   reg = rej(name=nm, address=em, number=pw)
   reg.save()
 else:
  fm = rejis()

 return render(request, 'app/mobile.html', {'form':fm})

def venue_Tpdf(request):
 buf = io.BytesIO()
 c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
 textob = c.beginText()
 textob.setTextOrigin(inch, inch)
 textob.setFont("Helvetica", 14)

 lines = [
  "This is previous year tax statement"
 ]

 venues = [p for p in Customer.objects.all() if p.user == request.user]
 lines = []
 for venue in venues:
  lines.append(venue.name)
  lines.append(venue.city)
  lines.append("NID Number:" + generate_random_number())
  lines.append("Total tax given:" + generate_random_numberT())
  break

 for line in lines:
  textob.textLine(line)

 c.drawText(textob)
 c.showPage()
 c.save()
 buf.seek(0)

 return FileResponse(buf, as_attachment=True, filename='vanue.pdf')

def search_venues(request):
 if request.method == "POST":
  searched = request.POST.get("searched")
  venues = Product.objects.filter(title__contains=searched)
  return render(request, 'app/search.html', {'searched':searched, 'venues':venues})
 else:
  return render(request, 'app/search.html', {})