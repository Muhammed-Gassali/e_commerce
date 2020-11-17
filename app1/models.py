from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class category(models.Model):
    category_name = models.CharField(max_length=100)

class products(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    price= models.IntegerField()
    description= models.CharField(max_length=500)
    image = models.ImageField(null=True, blank=True)

    @property
    def ImageURL(self):
        try:
            url= self.image.url
        except:
            url=''
        return url

# class cart(models.Model):

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) 
    address = models.CharField(max_length=300, null=True)
    city = models.CharField(max_length=300, null=True)
    state = models.CharField(max_length=300, null=True)
    zipcode = models.CharField(max_length=300, null=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.address



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True) 
    address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def ___str__(self):
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


    @property
    def shipping(self):
        shipping=True
        return shipping



class OrderItem(models.Model):
    product = models.ForeignKey(products, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

