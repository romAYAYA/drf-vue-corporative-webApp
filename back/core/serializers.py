from rest_framework import serializers
from rest_framework.fields import CharField
from . import models


class ProfileSerializer(serializers.ModelSerializer):
    username = CharField(source="user.username", required=True)
    email = CharField(source="user.email", required=True)

    class Meta:
        model = models.Profile
        fields = ("username", "email")
