from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
def upload_path(instance, filname):
    return '/'.join(['cover', str(instance.title), filname])

class User(AbstractUser):
    username = models.EmailField(max_length=30,unique=True)
    # username = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # email = models.EmailField(max_length=255,unique=True)
    phone=models.CharField(max_length=255,null=True)
    birth_date = models.DateField(null=True)

    # username = None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Customer(models.Model):
    # username = models.EmailField(unique=True, null=True)
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return self.email

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
    phone=models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
		
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

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
    customer =models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price =models.DecimalField(max_digits=10, decimal_places=2)