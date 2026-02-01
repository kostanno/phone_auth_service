from rest_framework import serializers
from .models import User, UserProfile
import phonenumbers
from django.utils.translation import gettext_lazy as _


class PhoneNumberValidator:
    """Валидатор номера телефона"""

    def __call__(self, value):
        try:
            phone = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(phone):
                raise serializers.ValidationError(_("неправильно введен номер телефона."))
            return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError(_("неверный формат телефона."))


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'email', 'is_verified', 'created_at')
        read_only_fields = ('id', 'is_verified', 'created_at')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    phone_number = serializers.CharField(
        source='user.phone_number',
        read_only=True
    )

    class Meta:
        model = UserProfile
        fields = (
            'id', 'user', 'phone_number', 'first_name', 'last_name',
            'role', 'avatar', 'date_of_birth'
        )
        read_only_fields = ('id', 'user', 'phone_number', 'role')


class UserCreateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        validators=[PhoneNumberValidator()],
        max_length=15
    )
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name')

    def create(self, validated_data):
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')

        user = User.objects.create_user(
            phone_number=validated_data['phone_number']
        )

        UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name
        )

        return user