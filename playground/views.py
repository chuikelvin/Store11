# from re import X
from django.shortcuts import render
from django.http import HttpResponse,FileResponse, Http404
# from .models import Product
from django.apps import apps
from django.contrib import admin

import uuid
# from django.db import models
from store.models import Product, Customer, Cart

# Product

# app_models = apps.get_app_config('store').get_models()
# for model in app_models:
#     if model == store:

#     print(model)
    # try:
    #     admin.site.register(model)
    # except AlreadyRegistered:
    #     pass


# Create your views here.

def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def product(request):
    Product_list = Product.objects.all()
    response = render(request, 'product.html',{'Product_list':Product_list})
    if not request.COOKIES.get("id"):
        unique_id = uuid.uuid4()
        response.set_cookie(key='id', value=unique_id)
    # print(request.COOKIES.get("device_id"))
    # if request.COOKIES['device_id'] != '':
    #     print("cookie exists")
    # username = request.COOKIES['device_id']
    # unique_id = uuid.uuid4()
    # # print(unique_id)
    # Product_list = Product.objects.all()
    # response = render(request, 'product.html',{'Product_list':Product_list})
    # # uuid.uuid4
    # response.set_cookie(key='id', value=1)
    # tutorial  = request.COOKIES['java-tutorial']  
    # return HttpResponse("java tutorials @: "+  tutorial);  
    return response
    return render(request, 'product.html',{'Product_list':Product_list})

def cart(request):
    request.session[0]='cart'
    sess = request.session[0]
    cart = Cart.objects.all()

    print(cart)
    # print(cart)
    # print(created)
    # order, created = Order.objects.get_or_create(customer=customer, complete=False)
    context ={"cart":cart}
    return render(request, 'cart.html', context)
    # {"status":status}
	# return render(request, 'cart.html', context)
    # return render(request, 'cart.html', context)

def pdf_view(request):
    try:
        return FileResponse(open(r"E:\Documents\Python\unchained\playground\static\Kelvin_Chui.pdf", 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        print ('File not found')
        raise Http404()
# class Register(View):
#     def post(self):
#         pass
#     def get(self):
#         return render(request, 'register.html')

def register(request):
    status = ""
    if request.method == 'POST':
        status = ""
        first_name = request.POST["firstName"]
        last_name = request.POST["lastName"]
        email = request.POST["email"]
        password = request.POST['password']
        
        if Customer.objects.filter(email=email).exists():
            status = 'user exists'
            return render(request, 'register.html',{"status":status})
        else:
            user = Customer(first_name=first_name, last_name= last_name, email= email)
            user.save()
            status = 'registered'
            return render(request, 'register.html',{"status":status})

    if request.method == 'GET':
        return render(request, 'register.html',{"status":status})

def sign(request):
    status = ""
    if request.method == 'POST':
        if 'signUp' in request.POST:
            print("sign up")
            first_name = request.POST["firstName"]
            last_name = request.POST["lastName"]
            email = request.POST["email"]
            password = request.POST['password']
        
            if Customer.objects.filter(email=email).exists():
                status = 'user exists'
                return render(request, 'sign.html',{"status":status})
            else:
                user = Customer(first_name=first_name, last_name= last_name, email= email)
                user.save()
                status = 'registered'
                return render(request, 'product.html',{"status":status})
        elif 'signIn' in request.POST:
            print("sign in")
            email = request.POST["email"]
            password = request.POST['password']
        
            if Customer.objects.filter(email=email).exists():
                status = 'success'
                return render(request, 'product.html',{"status":status})
            else:
                status = 'no user'
                return render(request, 'sign.html',{"status":status})

    if request.method == 'GET':
        return render(request, 'sign.html',{"status":status})