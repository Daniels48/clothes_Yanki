from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name="username", max_length=255, unique=True)
    email = models.EmailField(verbose_name="email address", null=True, blank=True)
    phone = models.CharField(verbose_name="phone number", max_length=30, null=True, blank=True)
    date_join = models.DateTimeField(verbose_name="data joined", auto_now=True)
    first_name = models.CharField(verbose_name='Имя', max_length=255, blank=True, null=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255, blank=True, null=True)
    address = models.CharField(verbose_name="Адресс", max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(verbose_name="verified", default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        unique_together = ("username", "email", "phone")
