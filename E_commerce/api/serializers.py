from rest_framework import serializers
from .models import Account, Product, Order, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )

class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Account
        fields = ('uuid', 'user', 'balance')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('uuid', 'name', 'cost', 'number_of_product', 'on_sale')

class OrderSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ('uuid', 'account', 'product', )
