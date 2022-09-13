from django.urls import path
from . import views
# from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
    path('', views.home ,name='home'),
    path('contact/', views.contact , name='contact'),
    path('about/',views.about ,name='about'),
    path('view-pdf/', views.pdf_view,name='pdf_view'),
    path('product/', views.product,name='product'),
    path('register/', views.register,name='register'),
    path('sign/',views.sign,name='sign'),
    path('cart/',views.cart,name='cart'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)