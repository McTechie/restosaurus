from rest_framework import serializers
from decimal import Decimal
from .models import MenuItem, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'slug', 'title')


class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory_count')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ('id', 'title', 'stock', 'price', 'price_after_tax', 'description', 'category_id', 'category')

    def calculate_tax(self, item: MenuItem):
        return item.price * Decimal(1.1)
