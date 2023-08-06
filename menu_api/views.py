from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .models import (
    MenuItem,
    Category,
    Order,
    OrderItem,
    Cart,
)
from .serializers import (
    MenuItemSerializer,
    CategorySerializer,
    OrderSerializer,
    OrderItemSerializer,
    CartSerializer,
)


class MenuItems(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (IsAuthenticated,)

    # let only admins create menu items
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(MenuItems, self).get_permissions()
    
    # let only managers to toggle `featured` field
    def perform_update(self, serializer):
        if self.request.user.groups.filter(name='manager').exists():
            serializer.save()
        else:
            serializer.save(featured=False)

    # browse menu items by category
    def get_queryset(self):
        category = self.request.query_params.get('category')

        if category:
            return MenuItem.objects.filter(category__slug=category.lower())
        else:
            return MenuItem.objects.all()
        
    def get(self, request, *args, **kwargs):
        offset = request.query_params.get('offset')
        limit = request.query_params.get('limit')
        sort_by = request.query_params.get('sort_by')

        offset = int(offset) if offset else 0
        limit = int(limit) if limit else 10

        if sort_by:
            menu_items = MenuItem.objects.all().order_by(sort_by)[offset:offset+limit]
        else:
            menu_items = MenuItem.objects.all()[offset:offset+limit]
        
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MenuItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (IsAuthenticated,)


class Categories(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super(Categories, self).get_permissions()


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)


class AssignOrder(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        delivery_crew_id = request.data.get('delivery_crew_id')

        if not order_id:
            return Response({'message': 'Order id must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        if not delivery_crew_id:
            return Response({'message': 'Delivery crew id must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.filter(id=order_id).first()

        if not order:
            return Response({'message': f'Order {order_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        delivery_crew = User.objects.filter(id=delivery_crew_id).first()

        if not delivery_crew:
            return Response({'message': f'Delivery crew {delivery_crew_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.groups.filter(name='manager').exists():
            return Response({'message': 'You are not authorized to assign orders'}, status=status.HTTP_401_UNAUTHORIZED)

        order.delivery_crew = delivery_crew
        order.save()

        return Response({'message': f'Order {order_id} assigned to {delivery_crew.username}'}, status=status.HTTP_200_OK)


class Orders(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.groups.filter(name='customer').exists():
            return Order.objects.filter(user=self.request.user)
        elif self.request.user.groups.filter(name='delivery crew').exists():
            return Order.objects.filter(delivery_crew=self.request.user)
        else:
            return Order.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)


class OrderItems(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        order_id = request.query_params.get('order_id')

        if not order_id:
            return Response({'message': 'Order id must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.filter(id=order_id).first()

        if not order:
            return Response({'message': f'Order {order_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        order_items = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItems(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='customer').exists():
            return Response({'message': 'You are not authorized to add items to cart'}, status=status.HTTP_401_UNAUTHORIZED)

        menu_item_id = request.data.get('menu_item_id')
        quantity = request.data.get('quantity')

        if not menu_item_id:
            return Response({'message': 'Menu item id must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        if not quantity:
            return Response({'message': 'Quantity must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        menu_item = MenuItem.objects.filter(id=menu_item_id).first()

        if not menu_item:
            return Response({'message': f'Menu item {menu_item_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        if menu_item.inventory_count < quantity:
            return Response({'message': f'Not enough stock for {menu_item.title}'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = Cart.objects.get_or_create(user=request.user, menu_item=menu_item)
        cart_item.quantity = quantity
        cart_item.unit_price = menu_item.price
        cart_item.price = menu_item.price * quantity
        cart_item.save()

        return Response({'message': f'Item {menu_item.title} added to cart'}, status=status.HTTP_200_OK)


class CustomerOrders(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        customer_id = request.data.get('customer_id')

        if not customer_id:
            return Response({'message': 'Customer id must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        customer = User.objects.filter(id=customer_id).first()

        if not customer:
            return Response({'message': f'Customer {customer_id} not found'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.groups.filter(name='manager').exists():
            return Response({'message': 'You are not authorized to view customer orders'}, status=status.HTTP_401_UNAUTHORIZED)

        orders = Order.objects.filter(user=customer)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
