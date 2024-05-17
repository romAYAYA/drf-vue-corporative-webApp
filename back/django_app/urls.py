from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django_app import views

urlpatterns = [
    # tokens
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    # auth
    path("api/register", views.user_register, name="user_register"),
    path("api/login", views.user_login, name="user_login"),
    path("api/users", views.get_users, name="get_users"),
    path("api/users/me", views.get_user, name="get_user"),
    path("api/users/update", views.update_user, name="update_user"),
]
