from django.urls import path
from .views import (
    UserProfileView,
    UserListView,
    UserDetailView,
    CreateUserView,
    UpdateUserRoleView
)

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', UserListView.as_view(), name='user-list'),
    path('<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('create/', CreateUserView.as_view(), name='user-create'),
    path('<int:user_id>/update-role/', UpdateUserRoleView.as_view(), name='update-user-role'),
]