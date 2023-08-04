from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import AccountSerializer, ProductSerializer, OrderSerializer, UserSerializer
from .models import Account, Product, Order
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication 

class AccountViewset(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    @action(detail=True, methods=['get'])
    def orders(self, request, pk, *args, **kwargs):
        try:
            account = Account.objects.get(id=pk)
        except:
            return Response({
                'message':'Account not found.',
            }, status=status.HTTP_404_NOT_FOUND)
        if account.user != request.user:
            return Response(
                {
                    'message': "You can't access another person's orders!"
                }
                , status=status.HTTP_403_FORBIDDEN
            )
        orders = account.order_set.all()
        serializer = OrderSerializer(data=orders, many=True)
        serializer.is_valid()
        return Response(
            {
                'message': 'Previous orders from your account',
                'number of orders': len(orders),
                'data': serializer.data,
                    
            }, status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get', 'delete'])
    def get_order(self, request, pk, uuid, *args, **kwargs):
        if request.method == "GET":
            try:
                account = Account.objects.get(id=pk)
            except:
                return Response({
                    'message':'Account not found.',
                }, status=status.HTTP_404_NOT_FOUND)
            if account.user != request.user:
                return Response(
                    {
                        'message': "You can't access another person's orders!"
                    }
                    , status=status.HTTP_403_FORBIDDEN
                )
            try:
                order = account.order_set.get(uuid=uuid)
            except:
                return Response({
                    'message':'Order not found.',
                }, status=status.HTTP_404_NOT_FOUND)
            serializer = OrderSerializer(order, many=False)
            return Response(
                {
                    'message': 'Previous order from your account',
                    'data': serializer.data,
                        
                }, status=status.HTTP_200_OK
            )
        else:
            try:
                account = Account.objects.get(id=pk)
            except:
                return Response({
                    'message':'Account not found.',
                }, status=status.HTTP_404_NOT_FOUND)
            if account.user != request.user:
                return Response(
                    {
                        'message': "You can't access another person's orders!"
                    }
                    , status=status.HTTP_403_FORBIDDEN
                )
            try:
                order = account.order_set.get(uuid=uuid)
            except:
                return Response({
                    'message':'Order not found.',
                }, status=status.HTTP_404_NOT_FOUND)
            order.delete()
            return Response(
                {
                    'message': f'Deleted order with uuid = {uuid} from your account',    
                }, status=status.HTTP_204_NO_CONTENT
            )

    
class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, )

class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    def create(self, request, *args, **kwargs):
        product_uuid = request.data['product_uuid']
        account_uuid = request.data['account_uuid']
        try:
            product = Product.objects.get(uuid=product_uuid)
            account = Account.objects.get(uuid=account_uuid)
        except Product.DoesNotExist:
            return Response({
                'message': "Product not found."
            }, status=status.HTTP_404_NOT_FOUND)
        except Account.DoesNotExist:
            return Response({
                'message': "Account not found."
            }, status=status.HTTP_404_NOT_FOUND)

        if product.number_of_product == 0:
            return Response({
                'message': "Sorry, this product isn't available. Please try again later!"
            }, status=status.HTTP_204_NO_CONTENT)
        cost = product.cost
        if product.on_sale:
            cost = product.perform_discount()
        if account.balance < cost:
            return Response({
                'message': "Sorry, there isn't enough money."
            }, status=status.HTTP_204_NO_CONTENT)
        
        order = Order.objects.create(account=account, product=product)
        order.save()
        serializer = OrderSerializer(order, many=False)           
        account.balance -= cost
        account.save()
        product.number_of_product -= 1
        product.save()
        return Response({
            'message': 'Successful Order',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    