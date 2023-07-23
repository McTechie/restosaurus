from django.urls import path
from .views import (
    Items,
    ItemDetail,
    Categories,
    CategoryDetail,
)


urlpatterns = [
    path("items/", Items.as_view()),
    path("items/<int:pk>/", ItemDetail.as_view()),
    path("categories/", Categories.as_view()),
    path("categories/<int:pk>/", CategoryDetail.as_view()),
]
