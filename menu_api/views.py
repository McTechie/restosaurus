from rest_framework import generics
from .models import Item, Category
from .serializers import ItemSerializer, CategorySerializer


class Items(generics.ListCreateAPIView):
    queryset = Item.objects.select_related('category').all()
    serializer_class = ItemSerializer


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class Categories(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
