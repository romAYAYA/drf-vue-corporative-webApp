from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes, api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django_app import models, serializers
from django_app.serializers import ProfileSerializer
from django_app.utils import password_check


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request: Request) -> Response:
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


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    try:
        profile = models.Profile.objects.get(user=user)
    except models.Profile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=404)

    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_users(request: Request) -> Response:
    users = User.objects.all()
    serialized_users = serializers.UserSerializer(instance=users, many=True).data
    return Response(serialized_users)
