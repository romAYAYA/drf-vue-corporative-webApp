import datetime

from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes, api_view
from django.contrib.auth import authenticate
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

from django_app import models, serializers
from django_app.utils import password_check, get_client_ip


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
