# apps/trading/views.py
from rest_framework import viewsets
from .models import Stock, Order
from .serializers import StockSerializer, OrderSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
