from rest_framework import serializers
from rest_framework.fields import CharField
from . import models


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ("bio", "avatar")


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = models.User
        fields = ("id", "username", "first_name", "last_name", "email", "profile")
