from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.serializers import PhoneNumberValidator

User = get_user_model()


class RequestCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=15,
        validators=[PhoneNumberValidator()]
    )


class VerifyCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(min_length=4, max_length=6)


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user_id = serializers.IntegerField()
    phone_number = serializers.CharField()
    is_verified = serializers.BooleanField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()