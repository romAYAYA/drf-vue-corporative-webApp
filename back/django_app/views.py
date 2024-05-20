import datetime

from django.contrib.auth.models import User
from django.db.models import Case, Sum, When, IntegerField
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import permission_classes, api_view
from django.contrib.auth import authenticate, logout
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

from django_app import models, serializers
from django_app.utils import (
    password_check,
    get_client_ip,
    update_rating,
    rate_item,
    get_item_rating,
)


def index(request):
    return render(request, "index.html")


@api_view(http_method_names=["GET", "POST"])
@permission_classes([AllowAny])
def api(request):
    if request.method == "GET":
        return Response(data={"message": "OK"})
    elif request.method == "POST":
        return Response(data={"message": request.data})


@api_view(["POST"])
@permission_classes([AllowAny])
def user_register(request: Request) -> Response:
    username = request.data.get("username", None)
    email = request.data.get("email", None)
    password = request.data.get("password", None)

    if not username or not email or not password:
        return Response(
            {"error": "Username, password or email not provided"}, status=400
        )

    if not password_check(password):
        return Response({"error": "Password is invalid"}, status=400)

    try:
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        serialized_user = serializers.UserSerializer(instance=user, many=False).data
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user": serialized_user,
            },
            status=201,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request: Request) -> Response:
    username = request.data.get("username", None)
    password = request.data.get("password", None)

    if not username or not password:
        return Response(
            {"error": "Username, password or email not provided"}, status=400
        )

    user = authenticate(request, username=username, password=password)

    login_count = models.Logs.objects.filter(
        user=user, date__gt=timezone.now() - datetime.timedelta(minutes=10)
    ).count()

    if login_count > 10:
        return Response({"error": "AYAYA, dont ddose"}, status=401)

    models.Logs.objects.create(
        user=user, ip_address=get_client_ip(request), date=timezone.now()
    )

    serialized_user = serializers.ProfileSerializer(
        models.Profile.objects.get(user=user), many=False
    ).data

    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": serialized_user,
        },
        status=201,
    )


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def update_user(request):
    try:
        user = request.user
    except User.DoesNotExist:
        return Response(status=404)

    if request.method == "GET":
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = serializers.UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    try:
        logout(request)
        return Response(status=205)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request: Request) -> Response:
    user = request.user
    serialized_user = serializers.UserSerializer(user)

    return Response(serialized_user.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_users(request: Request) -> Response:
    users = User.objects.all()
    serialized_users = serializers.UserSerializer(instance=users, many=True).data
    return Response(serialized_users)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_project(request: Request) -> Response:
    serializer = serializers.ProjectSerializer(data=request.data)
    if serializer.is_valid():
        project = serializer.save(author=request.user)
        return Response(serializers.ProjectSerializer(project).data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_projects(request):
    paginator = PageNumberPagination()
    paginator.page_size = 9
    projects = models.Project.objects.all()

    search_query = request.query_params.get("search", None)
    if search_query:
        projects = projects.filter(name__icontains=search_query)

    sort_by = request.query_params.get("sort_by", None)
    if sort_by == "name":
        projects = projects.order_by("name")
    elif sort_by == "ratings":
        projects = projects.annotate(
            rating_sum=Sum(
                Case(
                    When(ratings__is_liked=True, then=1),
                    When(ratings__is_liked=False, then=-1),
                    default=0,
                    output_field=IntegerField(),
                )
            )
        ).order_by("-rating_sum")
    elif sort_by == "creation_date":
        projects = projects.order_by("-creation_date")

    result_page = paginator.paginate_queryset(projects, request)
    serializer = serializers.ProjectSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_project_by_id(request: Request, project_id: int) -> Response:
    try:
        project = models.Project.objects.get(id=project_id)
    except models.Project.DoesNotExist:
        return Response({"detail": "Project not found."}, status=404)

    serializer = serializers.ProjectSerializer(project)
    return Response(serializer.data, status=200)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def edit_project(request: Request, project_id: int) -> Response:
    try:
        project = models.Project.objects.get(id=project_id, author=request.user)
    except models.Project.DoesNotExist:
        return Response(
            {
                "detail": "Project not found or you do not have permission to edit this project."
            },
            status=404,
        )

    serializer = serializers.ProjectSerializer(project, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_project(request: Request, project_id: int) -> Response:
    try:
        project = models.Project.objects.get(id=project_id, author=request.user)
    except models.Project.DoesNotExist:
        return Response(
            {
                "detail": "Project not found or you do not have permission to delete this project."
            },
            status=404,
        )

    project.delete()
    return Response({"detail": "Project deleted successfully."}, status=204)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def comment_list_create(request, project_id):
    project = get_object_or_404(models.Project, id=project_id)

    if request.method == "GET":
        comments = models.Comment.objects.filter(project=project)
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        data = request.data.copy()
        data["project"] = project.id
        serializer = serializers.CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_id):
    comment = get_object_or_404(models.Comment, id=comment_id)

    if request.method == "GET":
        serializer = serializers.CommentSerializer(comment)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = serializers.CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        comment.delete()
        return Response(status=204)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def rate_project(request, project_id):
    return rate_item(request, project_id, models.Project, models.ProjectRating)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def rate_comment(request, comment_id):
    return rate_item(request, comment_id, models.Comment, models.CommentRating)
