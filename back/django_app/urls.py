from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django_app import views

urlpatterns = [
    path("api/register", views.register, name="register"),
    path("api/users", views.get_users, name="get_users"),
    path("api/users_update", views.update_profile, name="update_profile"),
]
