from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = None
    email = models.EmailField(_("введите адрес почты"), blank=True)
    phone_number = models.CharField(_("номер телефона"), max_length=15, unique=True)
    is_verified = models.BooleanField(_("верификация"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'номер телефона'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("пользователь")
        verbose_name_plural = _("пользователи")

    def __str__(self):
        return self.phone_number


class UserProfile(models.Model):
    class UserRole(models.TextChoices):
        USER = 'user', _('пользователь')
        MODERATOR = 'moderator', _('модератор')
        ADMIN = 'admin', _('администратор')

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='профиль'
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.USER
    )
    avatar = models.ImageField(upload_to='фото/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = _("профиль пользователя")
        verbose_name_plural = _("профиль пользователей")

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name or self.last_name else self.user.phone_number

    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.UserRole.MODERATOR