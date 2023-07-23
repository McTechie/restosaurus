from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from .views import (
    RegisterView,
    AddUserToGroup,
    RemoveUserFromGroup,
    UserList,
)


urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token-blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("groups/", AddUserToGroup.as_view(), name="add_user_to_group"),
    path("groups/<int:pk>/", RemoveUserFromGroup.as_view(), name="remove_user_from_group"),
    path("users/", UserList.as_view(), name="user_list"),
]
