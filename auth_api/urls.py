from django.urls import path
from .views import (
    RequestAuthCodeView,
    VerifyCodeView,
    CustomTokenRefreshView,
    LogoutView,
    CheckCodeStatusView
)

urlpatterns = [
    path('request-code/', RequestAuthCodeView.as_view(), name='request-code'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check-code/', CheckCodeStatusView.as_view(), name='check-code'),
]