from rest_framework import serializers
from decimal import Decimal
from .models import Item, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'slug', 'title')


class ItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory_count')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'title', 'stock', 'price', 'price_after_tax', 'description', 'category_id', 'category')

    def calculate_tax(self, item: Item):
        return item.price * Decimal(1.1)
