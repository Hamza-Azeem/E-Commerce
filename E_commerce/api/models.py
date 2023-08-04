from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Account(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, max_digits=9)
    def __str__(self):
        return f'Name: {self.user.username} / Balance: {self.balance}'

class Product(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    cost = models.DecimalField(decimal_places=2, max_digits=9)
    number_of_product = models.IntegerField(default=0)
    on_sale = models.BooleanField()
    def perform_discount(self):
        cost = self.cost
        return cost - (cost / 10)
    def __str__(self):
        return f'Product: {self.name} / Cost: {self.cost}'

class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    def __str__(self):
        return f'AccountOf: {self.account.user.username} / ProductName: {self.product.name}'