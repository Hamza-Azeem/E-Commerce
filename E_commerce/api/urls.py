from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  AccountViewset, ProductViewset, OrderViewset
from rest_framework.authtoken.views import ObtainAuthToken

router = DefaultRouter()
router.register('accounts', AccountViewset)
router.register('products', ProductViewset)
router.register('orders', OrderViewset)
urlpatterns = [
    path('api/', include((router.urls))),
    path('api/getToken/', ObtainAuthToken.as_view(),),
    path('api/accounts/<int:pk>/get_order/<uuid:uuid>/', AccountViewset.as_view({'get': 'get_order', 'delete':'get_order'}),)
]