from django.urls import path
from . import views
# from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
    # path('', views.store ,name='home'),
    path('contact/', views.contact , name='contact'),
    path('about/',views.about ,name='about'),
    # path('view-pdf/', views.pdf_view,name='pdf_view'),
    path('',views.store ,name='store'),
    # path('product/', views.product,name='product'),
    path('register/', views.register,name='register'),
    path('sign/',views.sign,name='sign'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('payment/',views.payment,name='payment'),
    path('userhandler/',views.userhandler,name='userhandler'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)