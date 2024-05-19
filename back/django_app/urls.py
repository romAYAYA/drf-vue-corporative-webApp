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
    # projects
    path("api/projects/", views.get_all_projects, name="get_all_projects"),
    path(
        "api/projects/<int:project_id>/",
        views.get_project_by_id,
        name="get_project_by_id",
    ),
    path("api/projects/create", views.create_project, name="create_project"),
    path(
        "api/projects/<int:project_id>/edit/", views.edit_project, name="edit_project"
    ),
    path(
        "api/projects/<int:project_id>/delete/",
        views.delete_project,
        name="delete_project",
    ),
    #
    path(
        "api/projects/rating/<int:project_id>/", views.rate_project, name="rate_project"
    ),
    path(
        "api/comments/rating/<int:comment_id>/", views.rate_comment, name="rate_comment"
    ),
]
