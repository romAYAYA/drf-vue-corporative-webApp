from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Project


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("bio", "avatar")


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "profile")

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        profile_serializer = self.fields["profile"]

        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        profile_instance = instance.profile
        profile_serializer.update(profile_instance, profile_data)

        return instance


class ProjectSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Project
        fields = ["id", "name", "description", "creation_date", "author", "file"]
