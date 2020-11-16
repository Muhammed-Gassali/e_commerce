from django.contrib import admin
from django.contrib import messages
from .models import products,category,Order,OrderItem,ShippingAddress
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)