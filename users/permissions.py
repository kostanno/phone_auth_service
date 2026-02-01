from rest_framework import permissions


class IsVerifiedUser(permissions.BasePermission):
    """Разрешает доступ только верифицированным пользователям"""

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_verified
        )


class IsAdminUser(permissions.BasePermission):
    """Разрешает доступ только администраторам"""

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_staff
        )


class IsProfileOwnerOrAdmin(permissions.BasePermission):
    """Разрешает доступ владельцу профиля или администратору"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user


class RoleBasedPermission(permissions.BasePermission):
    """Разрешения на основе ролей"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        user_role = getattr(request.user.profile, 'role', 'user')
        if user_role == 'admin':
            return True
        elif user_role == 'moderator':
            return request.method in permissions.SAFE_METHODS + ('PUT', 'PATCH')
        elif user_role == 'user':

            return request.method in permissions.SAFE_METHODS
        return False