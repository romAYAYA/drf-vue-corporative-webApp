from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django_app import views

urlpatterns = [
    path("api/users", views.get_users, name="get_users"),
]
