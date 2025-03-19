# apps/trading/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'stocks', StockViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
