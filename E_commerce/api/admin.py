from django.contrib import admin
from .models import Account, Product, Order
# Register your models here.

admin.site.register(Account)
admin.site.register(Product)
admin.site.register(Order)