from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
def upload_path(instance, filname):
    return '/'.join(['cover', str(instance.title), filname])

def profile_upload_path(instance, filname):
    return '/'.join(['profile', str(instance.username), filname])

class User(AbstractUser):
    username = models.EmailField(max_length=30,unique=True)
    # username = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # email = models.EmailField(max_length=255,unique=True)
    phone=models.CharField(max_length=255,null=True)
    birth_date = models.DateField(null=True)
    profile_pic = models.ImageField(null=True, upload_to=profile_upload_path,default='/profile/user.png')

    # username = None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Product(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=upload_path)
    description = models.TextField()
    price = models.IntegerField()
    inventory_type = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title + "   " + self.description

class Address(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone=models.CharField(null=True,max_length=255)
    region = models.CharField(null=True,max_length=255)
    postal_address = models.CharField(null=True,max_length=255)
    city = models.CharField(null=True,max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.get_total for item in cartitems])
        return int(total) 

    @property
    def get_cart_items(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.quantity for item in cartitems])
        return int(total) 
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_cart_vat(self):
        # cartitems = self.cartitem_set.all()
        total = self.get_cart_total*0.06
        return int(total)
    
    @property
    def get_cart_shipping(self):
        # cartitems = self.cartitem_set.all()
        total = self.get_cart_total*0.02
        return int(total)

    @property
    def get_total_payable(self):
        # cartitems = self.cartitem_set.all()
        total = self.get_cart_total+self.get_cart_vat+self.get_cart_shipping
        return int(total)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return int(total)

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES=[
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at= models.DateTimeField(auto_now_add=True)
    payment_status =models.CharField(max_length=1 ,choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    order_id=models.CharField(max_length=255,unique=True)
    order_total= models.IntegerField()
    user =models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.order_id

    
    # def __str__(self):
    #     return self.title + "   " + self.description

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price =models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.order)