from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact , name='contact'),
    path('about/',views.about ,name='about'),
    path('',views.store ,name='store'),
    path('product/<int:id>', views.product_details,name='product_details'),
    path('sign/',views.sign,name='sign'),
    path('cart/',views.cart,name='cart'),
    path('userdetails/',views.userdetails,name='userdetails'),
    path('usercart/',views.usercart,name='usercart'),
    path('checkout/',views.checkout,name='checkout'),
    path('payment/',views.payment,name='payment'),
    # path('payorder/',views.payorder,name='pay'),
    path('userhandler/',views.userhandler,name='userhandler'),
    path('cart_handler/',views.cart_handler,name='cartHandler'),
    path('updatecart/',views.updatecart,name='updatecart'),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('order/',views.orders,name='order'),
]