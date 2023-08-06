from rest_framework import serializers
from decimal import Decimal
from auth_api.serializers import UserSerializer
from .models import (
    MenuItem,
    Category,
    Order,
    OrderItem,
)


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
    
    def create(self, validated_data):
        category = validated_data.pop('category_id')
        menu_item = MenuItem.objects.create(category=category, **validated_data)
        return menu_item


class OrderSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    delivery_crew = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'delivery_crew', 'status', 'total_price', 'date')


class OrderItemSerializer(serializers.Serializer):
    order = OrderSerializer(read_only=True)
    menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'menu_item', 'quantity', 'unit_price', 'price')


class CartSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'user', 'menu_item', 'quantity', 'unit_price', 'price')
