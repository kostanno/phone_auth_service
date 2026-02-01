from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import User, UserProfile
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserCreateSerializer
)
from .permissions import (
    IsProfileOwnerOrAdmin,
    IsVerifiedUser,
    RoleBasedPermission
)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """API для получения и обновления профиля пользователя."""
    serializer_class = UserProfileSerializer
    permission_classes = [IsVerifiedUser, IsProfileOwnerOrAdmin]

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)


class UserListView(generics.ListAPIView):
    """API для получения списка пользователей (только для администраторов)."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all().order_by('-created_at')


class UserDetailView(generics.RetrieveAPIView):
    """API для получения детальной информации о пользователе."""
    serializer_class = UserSerializer
    permission_classes = [IsVerifiedUser, RoleBasedPermission]
    queryset = User.objects.all()
    lookup_field = 'id'


class CreateUserView(generics.CreateAPIView):
    """API для создания нового пользователя."""
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []


class UpdateUserRoleView(APIView):
    """API для обновления роли пользователя"""
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        profile = user.profile

        new_role = request.data.get('role')
        if new_role not in dict(UserProfile.UserRole.choices):
            return Response(
                {'error': 'неправильные права'},
                status=status.HTTP_400_BAD_REQUEST
            )

        profile.role = new_role
        profile.save()

        return Response({
            'message': f'Role updated to {new_role}',
            'user_id': user.id,
            'phone_number': user.phone_number,
            'role': profile.role
        })