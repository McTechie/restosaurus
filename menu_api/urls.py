from django.urls import path
from .views import (
    MenuItems,
    MenuItemDetail,
    Categories,
    CategoryDetail,
    AssignOrder,
    Orders,
    OrderDetail,
    OrderItems,
    CartItems,
    CustomerOrders,
)


urlpatterns = [
    path("items/", MenuItems.as_view()),
    path("items/<int:pk>/", MenuItemDetail.as_view()),
    path("categories/", Categories.as_view()),
    path("categories/<int:pk>/", CategoryDetail.as_view()),
    path("assign-order/", AssignOrder.as_view()),
    path("orders/", Orders.as_view()),
    path("orders/<int:pk>/", OrderDetail.as_view()),
    path("orders/<int:pk>/items/", OrderItems.as_view()),
    path("cart/", CartItems.as_view()),
    path("customer-orders/", CustomerOrders.as_view()),
]
