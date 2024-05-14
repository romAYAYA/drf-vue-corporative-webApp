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
    path("api/users_register", views.user_register, name="user_register"),
    path("api/users_login", views.user_login, name="user_login"),
    path("api/users_update", views.update_profile, name="update_profile"),
    path("api/users", views.get_users, name="get_users"),
    path("api/user", views.get_user, name="get_user"),
]
