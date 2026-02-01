from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import get_user_model
from django.core.cache import cache

from .serializers import (
    RequestCodeSerializer,
    VerifyCodeSerializer,
    TokenSerializer,
    RefreshTokenSerializer,
    LogoutSerializer
)
from .services import (
    generate_otp,
    send_sms_mock,
    store_otp,
    verify_otp,
    get_remaining_time
)
from .throttling import (
    RequestCodeThrottle,
    VerifyCodeThrottle
)

User = get_user_model()


class RequestAuthCodeView(APIView):
    """API для запроса кода авторизации"""
    throttle_classes = [RequestCodeThrottle]
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RequestCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = generate_otp()
            store_otp(phone_number, code)
            send_sms_mock(phone_number, code)
            remaining_time = get_remaining_time(phone_number)
            return Response({
                'detail': 'Code sent successfully',
                'phone_number': phone_number,
                'code_expires_in': remaining_time,
                'note': 'In development mode, code is logged to console'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    """API для проверки кода и получения токенов."""
    throttle_classes = [VerifyCodeThrottle]
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']

            # Проверяем код
            is_valid, message = verify_otp(phone_number, code)

            if not is_valid:
                return Response(
                    {'detail': message},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Получаем или создаем пользователя
            user, created = User.objects.get_or_create(
                phone_number=phone_number
            )

            if created:
                user.set_unusable_password()
                user.save()
                from apps.users.models import UserProfile
                UserProfile.objects.create(user=user)

            # Обновляем статус верификации
            user.is_verified = True
            user.save()

            # Генерируем JWT токены
            refresh = RefreshToken.for_user(user)

            token_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'phone_number': user.phone_number,
                'is_verified': user.is_verified,
            }

            serializer = TokenSerializer(data=token_data)
            serializer.is_valid()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(TokenRefreshView):
    """API для обновления access токена."""
    serializer_class = RefreshTokenSerializer


class LogoutView(APIView):
    """API для выхода из системы."""

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.validated_data['refresh']
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(
                    {'detail': 'Successfully logged out'},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {'detail': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckCodeStatusView(APIView):
    """API для проверки статуса OTP кода."""
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response(
                {'detail': 'Phone number is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        remaining_time = get_remaining_time(phone_number)

        if remaining_time > 0:
            return Response({
                'detail': 'Code is active',
                'phone_number': phone_number,
                'expires_in': remaining_time
            })

        return Response({
            'detail': 'No active code found',
            'phone_number': phone_number
        }, status=status.HTTP_404_NOT_FOUND)