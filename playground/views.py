# from re import X
import re
from django.shortcuts import render,redirect
from django.http import HttpResponse,FileResponse, Http404
# from .models import Product
from django.apps import apps
from django.contrib import admin

import uuid
# from django.db import models
from store.models import Product, Customer, Cart


def is_logged_in(request):
    if request.session.has_key('status'):
        # print ("request.session['status']")
        if request.session['status'] == 1:
            # print('test')
            return {"user_status" :'bg-success','action':'sign out'}
        else :
            return {"user_status" :'bg-secondary','action':'sign in'}

    else:
        request.session['status'] = 0
        return {"user_status" :'bg-secondary','action':'sign in'}



# Create your views here.

# def home(request):
#     return render(request, 'home.html')

def contact(request):
    check= is_logged_in(request)
    return render(request, 'contact.html',check)

def about(request):
    check= is_logged_in(request)
    return render(request, 'about.html',check)

def store(request):
    check= is_logged_in(request)
    # product = Product.objects.get(id=pk)
    if request.method == 'POST':
        # status = ""
        product_name = request.POST["producttitle"]
        quantity = request.POST["quantity"]
        print("adding to cart")
        # email = request.POST["email"]
        # password = request.POST['password']
    # if request.method == 'GET':
    Product_list = Product.objects.all()
    check.update({'Product_list':Product_list})
    response = render(request, 'store.html',check)
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
    check= is_logged_in(request)
    # request.session[0]='cart'
    # sess = request.session[0]
    # cart = Cart.objects.all()

    # print(cart)
    # # print(cart)
    # # print(created)
    # # order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # context ={"cart":cart}
    return render(request, 'cart.html',check)
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

def checkout(request):
    print(request.path)
    if request.session['status'] == 0:
        return redirect('/sign/',request.path)
    check= is_logged_in(request)
    return render(request, 'checkout.html',check)

def payment(request):
    if request.session['status'] == 0:
        return redirect('/sign/')
    check= is_logged_in(request)
    # if request.session.has_key('status'):
    #     print (request.session['status'])
    #     if request.session['status'] == 'login':
    #         return render(request, 'payment.html', {"user_status" :'bg-success'})
            
    #   username = request.session['status']
    #   return render(request, 'loggedin.html', {"username" :'bg-secondary'})
#    else:
    #   return render(request, 'login.html', {})
    
    return render(request, 'payment.html',check)

def register(request):
    check= is_logged_in(request)
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

def sign(request,*args,**kwargs):
    print(**kwargs)
    check= is_logged_in(request)
    # if request.session.has_key('status'):
    #     print (request.session['status'])
    #     if request.session['status'] == 'login':
    #         return render(request, 'payment.html', {"user_status" :'bg-success'})
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
                print(status)
                request.session['status']=1
                return redirect('/')
                return render(request, 'store.html',check)
            else:
                status = 'no user'
                print(status)
                return redirect('/sign/')
                return render(request, 'store.html',{"status":status})

    if request.method == 'GET':
        print(check)
        return render(request, 'sign.html',check)

def userhandler(request):
    check= is_logged_in(request)
    print (check['action'])
    if check['action'] == 'sign out':
        try:
            request.session['status'] = 0
            # del request.session['username']
        except:
            pass
        return redirect('/')
    else:
        return redirect('/sign/')
        return render(request, 'sign.html',check)
        print (request.session['status'])
        if request.session['status'] == 'login':
            return render(request, 'payment.html', {"user_status" :'bg-success'})
