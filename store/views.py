import ast
import json
import os
import re
import sys
from time import sleep
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,FileResponse, Http404
from . import forms

from django_daraja.mpesa.core import MpesaClient

from daraja.darajaconn import lipa_na_mpesa
import sys

from django.views.decorators.csrf import csrf_exempt
 
# adding Folder_2 to the system path
sys.path.insert(0, 'e:\\Documents\\Python\\unchained-plp\\store\\daraja\\')

from collections import defaultdict

from django.contrib.auth import authenticate, login, logout

# from .models import Product
from django.apps import apps
from django.contrib import admin

import uuid
from store.models import Order, OrderItem, Product, User, Cart, CartItem, Address,MpesaPayment



def is_logged_in(request):
    state='visually-hidden'
    
    if request.user.is_authenticated:
        try:
            # request.session['cart']
            # print(request.session['cart'])
            cart =Cart.objects.get_or_create(user=request.user,complete=False)
            try:
                for prod, quantity in request.session['cart'].items():
                # print(key, val)
                    cart =Cart.objects.get(user=request.user)
                    product=Product.objects.get(id =prod)
        # print(product)
        # print(cart)
                    CartItem.objects.get_or_create(cart=cart,product=product,quantity=quantity)
                # sleep(10)
                    # print('exists')
                # else:
                # cartitem =CartItem.objects.get_or_create(cart=cart,product=product,quantity=val)
                # get_cartitem = CartItem.objects.get_or_create(cart=cart,product=product)
                #     get_cartitem.quantity=(get_cartitem.quantity+val)
                #     get_cartitem.save()
                del request.session['cart']
            except:
                request.session['cart']=defaultdict(lambda: 0)
                # print(request.session['cart'])
                    # request.session['cart']

                # print(get_cartitem.quantity)
            # else:
            #     cartitem,created =CartItem.objects.get_or_create(cart=cart,product=product,quantity=1)
        except:
            print('error')
        if Cart.objects.filter(user=request.user).exists():
            cartm =Cart.objects.get(user=request.user)
            # print(cartm)
            total=cartm.get_cart_total
            items =cartm.get_cart_items
            if items <= 0:
                items=''
                # state='visually-hidden'
            else:
                state=''


            # return render(request, 'checkout.html',check)
        else:
            items=''
            
            # return redirect('/userdetails/',request.path)
        
        # cartm,created =Cart.objects.get_or_create(user=request.user,complete=False)
        # items =cartm.get_cart_items
        # if request.method == 'POST' and request.is_ajax():
        #     return JsonResponse({'response':'sent'})
        return {"user_status" :'bg-success','action':'SIGN OUT','items_no':items,'cart':total,'visually':state}
    elif request.session.has_key('status'):
        items=0
        total=0
        try:
            # print(request.session['cart'])
            # items=0
            for prod, quantity in request.session['cart'].items():
                items+= int(quantity)
                product=Product.objects.get(id =prod)
                # print(product.price)
                total += product.price*int(quantity)
            # print(items)


            # print(total)
        # for items in cart.values():
        #     print(items)
            # print(value)


            if items>0:
                state=''
        except:
            print('error1')
        if request.session['status'] == 1:
            return {"user_status" :'bg-success','action':'SIGN OUT','items_no':items,'cart':total,'visually':state}
        else :
            return {"user_status" :'bg-secondary','action':'SIGN IN','items_no':items,'cart':total,'visually':state}

    else:
        # print(request.session['cart'])
        items=0
        try:
            # items=0
            for prod, quantity in request.session['cart'].items():
                items+= int(quantity)
            # print(items)
            if items>0:
                state=''
        except:
            print('error2')
        request.session['status'] = 0
        return {"user_status" :'bg-secondary','action':'SIGN IN','items_no':items,'visually':state}

def contact(request):
    check= is_logged_in(request)
    if request.method == 'POST':
        print(request.body)
    return render(request, 'contact.html',check)

def about(request):
    check= is_logged_in(request)
    return render(request, 'about.html',check)

def store(request):
    check= is_logged_in(request)
    try:
        request.session['cart']
    except:
        request.session['cart']=defaultdict(lambda: 0)
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = request.POST.get('product_id', False)
        # for productid,value in data.items():
            product=Product.objects.get(id=product_id)
            # print(request.user)
            cart,created =Cart.objects.get_or_create(user=request.user,complete=False)
            # print(cart)
            if CartItem.objects.filter(cart=cart,product=product).exists():
                get_cartitem = CartItem.objects.get(cart=cart,product=product)
                get_cartitem.quantity=(get_cartitem.quantity+1)
                get_cartitem.save()
                # check= is_logged_in(request)
                # print(get_cartitem.quantity)
            else:
                cartitem,created =CartItem.objects.get_or_create(cart=cart,product=product,quantity=1)
                # check= is_logged_in(request)
        else:
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
                cart_dict[product_id] = int(cart_dict.get(product_id))+1
            except KeyError:
                cart_dict[product_id] = 1
        # quantity = request.POST["quantity"]
        # print(cart_dict[product_id])
        # email = request.POST["email"]
            request.session['cart']=cart_dict
            # print(request.session['cart'])
        # password = request.POST['password']
    # if request.method == 'GET':
    Product_list = Product.objects.all()
    check= is_logged_in(request)
    check.update({'Product_list':Product_list})
    response = render(request, 'store.html',check) 
    return response
    # return render(request, 'product.html',{'Product_list':Product_list})

def usercart(request):
    if request.user.is_authenticated:
        try:
            # request.session['cart']
        # print(request.session['cart'])
            cart =Cart.objects.get_or_create(user=request.user,complete=False)
            for prod, quantity in request.session['cart'].items():
                # print(key, val)
                cart =Cart.objects.get(user=request.user)
                product=Product.objects.get(id =prod)
        # print(product)
        # print(cart)
                print(CartItem.objects.get_or_create(cart=cart,product=product,quantity=quantity))
                # sleep(10)
                    # print('exists')
                # else:
                # cartitem =CartItem.objects.get_or_create(cart=cart,product=product,quantity=val)
                # get_cartitem = CartItem.objects.get_or_create(cart=cart,product=product)
                #     get_cartitem.quantity=(get_cartitem.quantity+val)
                #     get_cartitem.save()
            del request.session['cart']
                # print(request.session['cart'])
                    # request.session['cart']

                # print(get_cartitem.quantity)
            # else:
            #     cartitem,created =CartItem.objects.get_or_create(cart=cart,product=product,quantity=1)
        except:
            print('error')
            # request.session['cart']=defaultdict(lambda: 0)
        
        # print(request.user)
        cartm,created =Cart.objects.get_or_create(user=request.user,complete=False)
        items =cartm.cartitem_set.all()
        if request.method == 'POST':
            product_id=int(request.POST['delete'])
            product=Product.objects.get(id=product_id)
            try:
                get_cartitem = CartItem.objects.get(cart=cartm,product=product)
                get_cartitem.delete()
            except:
                print()
            # get_cartitem.quantity=(get_cartitem.quantity+1)
        # check.update({'cart':items})
    # # print(created)
    # # order, created = Order.objects.get_or_create(user=user, complete=False)
    # context ={"cart":cart}
        # print(cartm.get_cart_total)
        check= is_logged_in(request)
        check.update({'cart':items,'total':cartm})
        return render(request, 'usercart.html',check)
    else:
        return redirect('/cart/')

def cart(request):
    if request.user.is_authenticated:
        try:
            request.session['cart']
        except:
            request.session['cart']=defaultdict(lambda: 0)
        return redirect('/usercart/')
        check= is_logged_in(request)
        # print(request.user)
        cartm,created =Cart.objects.get_or_create(user=request.user,complete=False)
        items =cartm.cartitem_set.all()
        check.update({'cart':items})
    # # print(created)
    # # order, created = Order.objects.get_or_create(user=user, complete=False)
    # context ={"cart":cart}
        print(items)
    # check.update({'cart':request.session['cart']})
        return render(request, 'cart.html',check)
        # customer=
    else:
       
        try:
            request.session['cart']
        except:
            request.session['cart']=defaultdict(lambda: 0)

    if request.method == 'POST':
        
        key = request.session['cart']
        value = str(request.POST['delete'])
        value.replace(" ", "")
        value.strip()
        # print(request.session['cart'])
        # print(value)
        # key[value] = key.get(value)+1
        try:
            key.pop(value)
            request.session['cart']=key
        except:
            print()
        # cart_dictrequest.session['cart']
        
        # cart_dict=defaultdict(lambda: 0)
        # if request.session['cart'] is None:
        #     request.session['cart']=defaultdict(lambda: 0)

        

    # print(request.session['cart'])
    cart_items={}
    cart={}
    total_cost=0
    for key, val in request.session['cart'].items():
        
        
        cart_items[key]=Product.objects.filter(id =key)
        # for item, value in cart_items:
        #     print(value.cost)
        # print(cart_items[key].cost)
        # item_cost=Product.objects.all().values('eng_name','rank')
        cart[cart_items[key]]=val

        # for item in cart:
        #     print(item)
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
    check= is_logged_in(request)
    check.update({'cart':cart})
    for items,values in cart.items():
        for details in items:
            # print(details.price)
            # total_cost=5
            # print(int(values))
            total_cost += details.price*int(values)
            # print(total_cost)
        # for items in cart.values():
        #     print(items)
            # print(value)

    # print(cart)
    check.update({'total':total_cost})
    # # print(created)
    # # order, created = Order.objects.get_or_create(user=user, complete=False)
    # context ={"cart":cart}
    # print(check)
    # check.update({'cart':request.session['cart']})
    return render(request, 'cart.html',check)
    # {"status":status}
	# return render(request, 'cart.html', context)
    # return render(request, 'cart.html', context)

def checkout(request):
    # print(request.path)
    if request.user.is_authenticated:
        check= is_logged_in(request)
        # print(request.user)
        cartm,created =Cart.objects.get_or_create(user=request.user,complete=False)
        items =cartm.cartitem_set.all()
        check.update({'cart':items})
        if Address.objects.filter(user=request.user).exists():
            address =Address.objects.get(user=request.user)
            check.update({'details':address,'cart':items,'total':cartm})
            return render(request, 'checkout.html',check)
        else:
            return redirect('/userdetails/',request.path)
    # # print(created)
    # # order, created = Order.objects.get_or_create(user=user, complete=False)
    # context ={"cart":cart}
        print(cartm.get_cart_total)
    # check.update({'cart':request.session['cart']})
        return render(request, 'checkout.html',{'cart':items,'total':cartm})
    if request.session['status'] == 0:
        return redirect('/sign/',request.path)
    # check= is_logged_in(request)
    # return render(request, 'checkout.html',check)

def payment(request):
    if request.user.is_authenticated:
        check= is_logged_in(request)
        # print(request.user)
        cartm,created =Cart.objects.get_or_create(user=request.user,complete=False)
        # items =cartm.cartitem_set.all()
        # check.update({'cart':items})
    # # print(created)
    # # order, created = Order.objects.get_or_create(user=user, complete=False)
    # context ={"cart":cart}
        ammount=cartm.get_total_payable
        if ammount <=0:
            return redirect('/',request.path)
        # print(ammount)

        if request.method == 'POST':
            print("posted")
            number = request.POST["number"]
            if number[0] == '0':
                number = number.replace("0", "254", 1)
            

        # elif (number[0] == '7'):
        #     number = number.replace("7", "2547", 1)

        # text = text.replace("very", "not very", 1)
        # print(number)
            response,state=lipa_na_mpesa(number,ammount,'store11 #54lkjl')
            return JsonResponse({'response':'sent'})
    # if request.session.has_key('status'):
    #     print (request.session['status'])
    #     if request.session['status'] == 'login':
    #         return render(request, 'payment.html', {"user_status" :'bg-success'})
            
    #   username = request.session['status']
    #   return render(request, 'loggedin.html', {"username" :'bg-secondary'})
    else:
      return render(request, 'sign.html')
    check.update({'total':cartm})
    
    return render(request, 'payment.html',check)
    
    # return render(request, 'payment.html',check)

# def register(request):
#     check= is_logged_in(request)
#     status = ""
#     if request.method == 'POST':
#         status = ""
#         first_name = request.POST["firstName"]
#         last_name = request.POST["lastName"]
#         email = request.POST["email"]
#         password = request.POST['password']
        
#         if User.objects.filter(email=email).exists():
#             status = 'user exists'
#             return render(request, 'register.html',{"status":status})
#         else:
#             user = User(first_name=first_name, last_name= last_name, email= email)
#             user.save()
#             status = 'registered'
#             return render(request, 'register.html',{"status":status})

#     if request.method == 'GET':
#         return render(request, 'register.html',{"status":status})

def sign(request):
    if request.user.is_authenticated:
        return redirect('/userdetails/',request.path)
    check= is_logged_in(request)
    # login= forms.UserForm()
    # if request.session.has_key('status'):
    #     print (request.session['status'])
    #     if request.session['status'] == 'login':
    #         return render(request, 'payment.html', {"user_status" :'bg-success'})
    status = ""
    # return JsonResponse(check['items_no'],safe=False)
    if request.method == 'POST':
        if request.POST['form'] == 'signup':
            print (request.POST['form'])
            # return JsonResponse("signup",safe=False)
        # return JsonResponse("post",safe=False)
        # if 'signUp' in request.POST:
            first_name = request.POST["firstName"]
            last_name = request.POST["lastName"]
            username = request.POST["email"]
            password = make_password(request.POST['password'])
        
            if User.objects.filter(username=username).exists():
                status = 'user exists'
                print("exists")
                return JsonResponse('user already exists',safe=False)
                return render(request, 'sign.html/',{"status":status})
            else:
                user = User(first_name=first_name, last_name= last_name, username= username,password=password)
                user.save()
                address= Address(first_name=first_name, last_name=last_name,user=user)
                address.save()
                
                status = 'registered'
                return JsonResponse('Account created successfully',safe=False)
                return render(request, 'sign.html',{"status":status})
        # elif 'signIn' in request.POST:
        if request.POST['form'] == 'signin':
            username = request.POST["email"]
            password = request.POST['password']

            # print(username)

            user =authenticate(username =username,password=password)
            if user is not None:
                login(request, user)
        
            # if User.objects.filter(username=username).exists():
                status = 'success'
                print(status)
                request.session['status']=1
                # return redirect(request.META['HTTP_REFERER'])
                return JsonResponse('logged in',safe=False)
                return redirect('/')
                # return render(request, 'store.html',check)
            else:
                status = 'no user'
                print(status)
                return JsonResponse('invalid credentials',safe=False)
                return redirect('/')
                # return render(request, 'store.html',{"status":status})

    if request.method == 'GET':
        # print(check)
        return render(request, 'sign.html',check)

def userhandler(request):
    check= is_logged_in(request)
    # print (check['action'])
    if check['action'] == 'SIGN OUT':
        try:
            logout(request)
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
    check= is_logged_in(request)
    # key = request.session['cart']
    # value = request.POST['ref']
    # print(check['items_no'])
    # value=value.replace("{",'')
    # value=value.replace("}",'')
    # value=value.replace("\"",'')
    # value=value.replace("\r","")
    # value=value.replace("\n","")
    # value =value.strip('\r\n')
    # value =value.strip('\r')
    # value =value.strip('\n')
    # print(check['items_no'])

    # data=json.loads(str(value))

    # str = " Jan = January; Feb = February; Mar = March"
    # dictionary = dict(subString.split("=") for subString in str.split(";"))
    # print(dictionary)

    # data = dict(subString.split(":") for subString in value.split(","))

    # data = ast.literal_eval(value)

    # data = json.load(value)

    # ser_instance = serializers.serialize('json', [ value ])

    # print(data)
    # print(request.session['cart'])
    # for items,values in value.items():
    #     print(values)
    if request.method == 'POST':
        action = request.POST['action']
        # if action == 'add':
            # key[value] = key.get(value)+1
            # print(request.GET['ref'])
            # key.get(product_id)+1
            # key[value] =key[value]+1
            # print(key[value])
        # if action == 'remove':
            # key[value] = key.get(value)+1
            # key.pop(value)
# print(myDict);
            # print(key)
            # print(request.session['cart'])
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
        return JsonResponse(check['items_no'],safe=False)
        #    return HttpResponse("Request method is not a GET")


def product_details(request,id):
    check= is_logged_in(request)
    product=Product.objects.get(id=id)
    check.update({'product': product})
    return render(request, 'product.html',check)

def updatecart(request):
    data =json.loads(request.body)
    refresh= False
    if request.user.is_authenticated:
        for productid,value in data.items():
            product=Product.objects.get(id=productid)
            # print(request.user)
            cart,created =Cart.objects.get_or_create(user=request.user,complete=False)
            if int(value)<=0:
                refresh = True
            print(value)
            cartitem,created =CartItem.objects.get_or_create(cart=cart,product=product)
            cartitem.quantity = (value)
            cartitem.save()
            if int(cartitem.quantity) <= 0:
                cartitem.delete()
        
        check= is_logged_in(request)
        if refresh == True:
            # print('refresh')
            return render(request, 'cart.html',check)
        data=dict()
        data['items_no']=check['items_no']
        data['total']=check['cart']
            # print(data)
        return JsonResponse(data,safe=False)
    else:
        key = request.session['cart']
        # print(key)
        # print(data)
        request.session['cart']=data
        check= is_logged_in(request)
        print(check)
        data=dict()
        data['items_no']=check['items_no']
        data['total']=check['cart']
    # print(data['2'])
    return JsonResponse(data,safe=False)

def userdetails(request):
    if request.user.is_authenticated:
        check= is_logged_in(request)
        if request.method == 'POST':
            if 'update_user' in request.POST:
                user=User.objects.get(username=request.user)
                first_name = request.POST["fname"]
                last_name = request.POST["lname"]
                birth_date = request.POST["birth_date"]
                phone = request.POST["number"]

                user.first_name=(first_name) 
                user.last_name= (last_name)
                user.birth_date=(birth_date) 
                user.phone=(phone)
                try:
                    upload = request.FILES['prof_pic']
                    user.profile_pic= (upload)
                except:
                    noidea='filler'
                user.save()
            elif 'update_address' in request.POST:
                first_name = request.POST["fname"]
                last_name = request.POST["lname"]
                region = request.POST["region"]
                phone = request.POST["number"]
                city = request.POST["city"]
                postal_address = request.POST["postal_address"]

                if Address.objects.filter(user=request.user).exists():
                    address =Address.objects.get(user=request.user)

                    address.first_name = (first_name)
                    address.last_name = (last_name)
                    address.region = (region)
                    address.phone = (phone)
                    address.city = (city)
                    address.postal_address=(postal_address)
                    address.save()
                else:
                    address =Address.objects.get_or_create(user=request.user,first_name=first_name, last_name= last_name,region=region,phone=phone,city=city,postal_address=postal_address)
                check.update({'details':address})
                # sleep(0.2)
            return redirect('/userdetails/')
            return render(request, 'userdetails.html',check)
        else:               
            if Address.objects.filter(user=request.user).exists():
                address =Address.objects.get(user=request.user)
                check.update({'address':address,'details':(request.user.birth_date),'readonly':'disabled'})
                # return render(request, 'userdetails.html',check)
            if Order.objects.filter(user=request.user).exists():
                orders=Order.objects.filter(user=request.user)
                # order=Order.objects.get(user=request.user,order_id='#614a74')
                # ordereditem=OrderItem.objects.get(order_id=order,product=2)
                order_item =OrderItem.objects.all()
                # print(ordereditem.get_total())
                check.update({'orders':orders,'order_items': order_item})
                # print(order)
            # else:
                # check.update({'address':address,'readonly':'disabled'})
            return render(request, 'userdetails.html',check)
            # return render(request, 'userdetails.html',{'address':address,'readonly':'disabled'})
        
    else:
        return redirect('/sign/')


def getpaymentstatus(request):
    try:
        result=json.loads(request.body)
        # bodydata=result['Body']
        # print(result['order_id'])
        order_id=result['order_id']
    except:
        order_id=request.GET['order_id']
    order=Order.objects.get(order_id=order_id)
    # print(order.payment_status)
    if order.payment_status == 'F':
        return JsonResponse({'order':0})
    elif order.payment_status == 'C':
        return JsonResponse({'order':1})
    else:
        return JsonResponse({'order':'P'})
    # return JsonResponse({'order':1})

@csrf_exempt
def placeorder(request):
    if request.method == 'POST':
        try:
            result=json.loads(request.body)
            bodydata=result['Body']
            for key,value in bodydata.items():
                # print(key)
                print(value)
                if value['ResultCode'] != 0:
                    mpesa = MpesaPayment.objects.get(checkoutrequestid=value['CheckoutRequestID'])
                    mpesa.payment_status='F'
                    order_id=mpesa.order_id
                    order=Order.objects.get(order_id=order_id)
                    order.payment_status='F'
                    order.save()
                    mpesa.save()
                    # return JsonResponse({'order':'unsuccessful'})
                else:
                    mpesa = MpesaPayment.objects.get_or_create(checkoutrequestid=value['CheckoutRequestID'])
                    mpesa.payment_status='C'
                    mpesa.save()
                    # return JsonResponse({'order':'successful'})
            # if result != 0:
                # print("payment failed")
            # print(result['stkCallback'])
        except ValueError as e:
            print("NOT JSON")
        # print(request.body)
    if request.user.is_authenticated:
        if request.method == 'POST' and 'pay' in request.POST:
            # print(request.POST)
            # if 'pay' in request.POST:
            #     print('pay')
            order_id='#'
            order_id+= str(uuid.uuid4())[:6]
            cartitems =Cart.objects.get(user=request.user)
            items =cartitems.cartitem_set.all()
            order_total=cartitems.get_total_payable
            order =Order.objects.get_or_create(user=request.user,order_id=order_id,order_total=order_total)
            phone = request.POST["number"]
            if phone[0] == '0':
                phone = phone.replace("0", "254", 1)
            # # for order in order:
            # print(items)
            for item in items:
                product=item.product
                quantity=item.quantity
                # if quantity <= 0:
                #     print(quantity)
                #     return redirect('/')
                unit_price=item.product.price
                get_cartitem = OrderItem.objects.get_or_create(order=order[0],product=product,quantity=quantity,unit_price=unit_price)
                # printquantity)
            
            domain=request.get_host()
            callback_url= "https://"+domain+request.get_full_path()
            # callback_url="https://thawing-springs-95517.herokuapp.com/"
            # print(url)
            cl = MpesaClient()
            account_reference = order_id
            transaction_desc = 'Description'
            try:
                response = cl.stk_push(phone, order_total, account_reference, transaction_desc, callback_url)
                responsedict=json.loads(response.text)
                print(response.text)
                checkoutrequestid =responsedict['CheckoutRequestID']
                # print(checkoutrequestid)
                order =Order.objects.get(order_id=order_id)
                Mpesa = MpesaPayment.objects.get_or_create(order_id=order,checkoutrequestid=checkoutrequestid)
                state=True
            except:
                state=False

            
            # return HttpResponse(response)
            # get_cartitem = OrderItem.objects.get_or_create(order=order,product=product)
            # orderitem=items.orderitem_set.all()
            cartitems.delete()
            # response,state=lipa_na_mpesa(phone,order_total,'store11 #54lkjl',url)
            # print ('store11 '+order_id)
            return JsonResponse({'order':order_id,'state':state})
    else:
        return redirect('/')

def orders(request):
    if request.user.is_authenticated:
        order =Order.objects.filter(user=request.user)
        for items in order:
            print(items)
        # print(order.order_id)
        return render(request, 'orders.html',{'order':order})
    else:
        return redirect('/')


        cartm,created =Cart.objects.get_or_create(user=request.user,complete=False)
        items =cartm.cartitem_set.all()
        if request.method == 'POST':
            product_id=int(request.POST['delete'])
            product=Product.objects.get(id=product_id)
            get_cartitem = CartItem.objects.get(cart=cartm,product=product)
            get_cartitem.delete()
            # get_cartitem.quantity=(get_cartitem.quantity+1)
        # check.update({'cart':items})
    # # print(created)
    # # order, created = Order.objects.get_or_create(user=user, complete=False)
    # context ={"cart":cart}
        # print(cartm.get_cart_total)
        check.update({'cart':items,'total':cartm})