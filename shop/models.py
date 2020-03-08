from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default='')
    subcategory = models.CharField(max_length=50, default='')
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default='default.jpg')

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default='')
    email = models.EmailField(max_length=50, default='')
    phone = models.IntegerField( default='')
    message = models.CharField(max_length=50, default='')
    dateTime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.CharField(primary_key=True, max_length=20)
    items = models.CharField(max_length=5000, default='')
    name = models.CharField(max_length=50, default='')
    email = models.EmailField(max_length=50, default='')
    phone = models.IntegerField(default='')
    address = models.CharField(max_length=200, default='')
    state = models.CharField(max_length=200, default='')
    zip = models.IntegerField(default='')
    payment_status = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    dateTime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.order_id