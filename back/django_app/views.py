from rest_framework.decorators import permission_classes, api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from django_app import models, serializers


@api_view(["GET"])
@permission_classes([AllowAny])
def get_users(request: Request) -> Response:
    users = models.User.objects.all()
    serialized_users = serializers.UserSerializer(instance=users, many=True).data
    return Response(serialized_users)
