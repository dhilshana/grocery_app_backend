from django.db import models
from django . utils import timezone
from cloudinary . models import CloudinaryField

# Create your models here.

class Login(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=20,default='user')

class Registration(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length=20)
    number = models.IntegerField()
    role = models.CharField(max_length=20,default='user')

    login_id = models.OneToOneField(Login,on_delete=models.CASCADE)

class Category(models.Model):
    category_name = models.CharField(max_length=30)
    category_image = models.URLField('category')



class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.CharField(max_length=10)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.URLField('image')
    quantity = models.DecimalField(decimal_places=2,default=1.00,max_digits=5)
    unit = models.CharField(max_length=10,default='Kg')
    desc = models.TextField(default='description')



class Review(models.Model):
    product_id = models.CharField(max_length=10)
    user_id = models.CharField(max_length=10)
    product_name = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20)
    time = models.DateTimeField(default=timezone.now, auto_created=True)
    description = models.TextField()
    rating = models.PositiveSmallIntegerField(default=1, help_text="Rating should be between 1 and 5")


class Wishlist(models.Model):
    product_id = models.CharField(max_length=10)
    user_id = models.CharField(max_length=10)
    product_name = models.CharField(max_length=20)
    product_price = models.CharField(max_length=10)
    product_image = models.URLField('image')

class Cart(models.Model):
    product_id = models.CharField(max_length=10)
    user_id = models.CharField(max_length=10)
    product_name = models.CharField(max_length=20)
    product_price = models.CharField(max_length=10)
    product_image = models.URLField('image')
    cart_status = models.CharField(default=1,max_length=10)
    quantity = models.IntegerField(default=1)
    unit = models.CharField(max_length=10,default='Kg')

class Order(models.Model):
    product_id = models.CharField(max_length=10)
    user_id = models.CharField(max_length=10)
    product_name = models.CharField(max_length=20)
    product_price = models.CharField(max_length=10)
    product_image = models.URLField('image')
    quantity = models.IntegerField(default=1)
    order_status = models.CharField(default=1,max_length=10)
    unit = models.CharField(default='Kg',max_length=10)


class Address(models.Model):
    user_id = models.CharField(max_length=10)
    contact_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length = 12)
    street_address1 = models.CharField(max_length=30)
    street_address2  = models.CharField(max_length=30)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    isDefault = models.BooleanField(default=False)
    


