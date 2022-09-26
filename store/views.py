# from re import X
# import re
from django.shortcuts import render,redirect
from django.http import HttpResponse,FileResponse, Http404
from . import forms

from collections import defaultdict

from django.contrib.auth import authenticate, login, logout

# from .models import Product
from django.apps import apps
from django.contrib import admin

import uuid
from store.models import Product, User, Cart



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
    # print(request.user)
    try:
        request.session['cart']
    except:
        request.session['cart']=defaultdict(lambda: 0)

    # request.session['cart']=defaultdict(lambda: 0)
    # product = Product.objects.get(id=pk)
    if request.method == 'POST':
        # cart_dict=defaultdict(lambda: 0)
        # if request.session['cart'] is None:
        #     request.session['cart']=defaultdict(lambda: 0)

        cart_dict=request.session['cart']
        # request.session['status'] = cart_dict
        # if request.user.is_authenticated():
        #     print('gg')
        # cart_dict=defaultdict(lambda: 0)

        # status = ""
        
        product_id = request.POST.get('product_id', False)
        # print(cart_dict)
        # if cart_dict.get(product_id) == '':
        #     cart_dict[product_id] = 0
        # # test_dict['best'] = test_dict.get('best', 0) + 3
        # cart_dict.setdefault([product_id], 0)
        # print(cart_dict[product_id])
        try:
            cart_dict[product_id]
            cart_dict[product_id] = cart_dict.get(product_id)+1
        except KeyError:
            cart_dict[product_id] = 1
        # quantity = request.POST["quantity"]
        # print(cart_dict[product_id])
        # email = request.POST["email"]
        request.session['cart']=cart_dict
        print(request.session['cart'])
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
    try:
        request.session['cart']
    except:
        request.session['cart']=defaultdict(lambda: 0)

    # print(request.session['cart'])
    cart_items={}
    cart={}

    for key, val in request.session['cart'].items():
        
        
        cart_items[key]=Product.objects.filter(id =key)
        cart[cart_items[key]]=val
        # cart=Product.objects.filter(id =key)
        # cart.append({cart_items:val})
        # cart.append(Product.objects.filter(id =key))
        # check.update({'cart':cart,'quantity':val})
        # print(cart_items)
        # print(cart)
        # cart[cart_items]=val
        # for key, val in cart_items:
            # print(key)
        # check.update({'cart':cart_items,'quantity':val})
        # print(cart)
    # request.session[0]='cart'
    # sess = request.session[0]
    # cart = Cart.objects.all()
    # check.update({'cart':cart_items,'quantity':val})
    # print(cart_items)
    # print(cart)
    check.update({'cart':cart})
    # # print(cart)
    # # print(created)
    # # order, created = Order.objects.get_or_create(user=user, complete=False)
    # context ={"cart":cart}
    print(check)
    # check.update({'cart':request.session['cart']})
    return render(request, 'cart.html',check)
    # {"status":status}
	# return render(request, 'cart.html', context)
    # return render(request, 'cart.html', context)

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
        
        if User.objects.filter(email=email).exists():
            status = 'user exists'
            return render(request, 'register.html',{"status":status})
        else:
            user = User(first_name=first_name, last_name= last_name, email= email)
            user.save()
            status = 'registered'
            return render(request, 'register.html',{"status":status})

    if request.method == 'GET':
        return render(request, 'register.html',{"status":status})

def sign(request):
    # print(**kwargs)
    check= is_logged_in(request)
    # login= forms.UserForm()
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
        
            if User.objects.filter(email=email).exists():
                status = 'user exists'
                return render(request, 'sign.html',{"status":status})
            else:
                user = User(first_name=first_name, last_name= last_name, email= email)
                user.save()
                status = 'registered'
                return render(request, 'product.html',{"status":status})
        elif 'signIn' in request.POST:
            print("sign in")
            email = request.POST["email"]
            password = request.POST['password']
        
            if User.objects.filter(email=email).exists():
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


def cart_handler(request):
    print('accessed')
    if request.method == 'GET':
        action = request.GET['action']
        # inputtype = request.POST.get('action', None)
        # payload = {"response":str(inputtype)} if inputtype is not None else {"response":"please type something"}
        print(action)
        #    post_id = request.GET['post_id']
        #    likedpost = Post.objects.get(pk=post_id) #getting the liked posts
        #    m = Like(post=likedpost) # Creating Like Object
        #    m.save()  # saving it to store in database
        return HttpResponse("Success!") # Sending an success response
        return redirect('/')
    else:
           return HttpResponse("Request method is not a GET")