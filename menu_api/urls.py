from django.urls import path
from .views import (
    MenuItems,
    MenuItemDetail,
    Categories,
    CategoryDetail,
)


urlpatterns = [
    path("items/", MenuItems.as_view()),
    path("items/<int:pk>/", MenuItemDetail.as_view()),
    path("categories/", Categories.as_view()),
    path("categories/<int:pk>/", CategoryDetail.as_view()),
]
