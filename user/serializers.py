from rest_framework import serializers
from .models import User


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["role", "username", "email", "password"]


class Profileserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "address"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)