from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from clothes.models import BaseProduct, Product

from users.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name="username", max_length=255, unique=True)
    email = models.EmailField(verbose_name="email address", blank=True, unique=True)
    phone = models.CharField(verbose_name="phone number", max_length=30, blank=True, unique=True)
    date_join = models.DateTimeField(verbose_name="data joined", auto_now_add=True)
    first_name = models.CharField(verbose_name='Имя', max_length=255, blank=True, null=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255, blank=True, null=True)
    city = models.CharField(verbose_name="Город", max_length=255, blank=True, null=True)
    post_office = models.CharField(verbose_name="Адресс почты", max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(verbose_name="verified", default=False)
    like_list = models.ManyToManyField(BaseProduct, related_name="Like_list")
    cart_list = models.ManyToManyField(Product, related_name="Cart_list", through="CartProduct")
    currency = models.CharField(max_length=15, default="UAH", verbose_name="Currency")

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        unique_together = ("username", "email", "phone")


# class Orders(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, db_index=True)
#     email = models.EmailField(verbose_name="email address", blank=True, db_index=True)
#     first_name = models.CharField(max_length=255, db_index=True)
#     last_name = models.CharField(max_length=255, db_index=True)
#     delivery_method = models.ForeignKey("Delivery_methods", related_name="deliverys_method", on_delete=models.CASCADE)
#     phone = models.CharField(max_length=255)
#     pay_method = models.ForeignKey("Pay_methods", related_name="pays_method", on_delete=models.CASCADE)
#     status_pay = models.ForeignKey("Pay_status",on_delete=models.CASCADE)
#     status = models.ForeignKey("Pay_methods", on_delete=models.CASCADE, default=1)
#     sum_order = models.DecimalField(max_digits=10, decimal_places=2)
#     currency = models.CharField(max_length=15)
#     date_order = models.DateTimeField(verbose_name="data order", auto_now=True)
#     clothes = models.ManyToManyField(Product, through="OrderProduct")
#
#
# class Delivery_methods(models.Model):
#     name = models.CharField(max_length=255, db_index=True)
#
#
# class Pay_methods(models.Model):
#     name = models.CharField(max_length=255, db_index=True)
#
#
# class List_status(models.Model):
#     name = models.CharField(max_length=255, db_index=True)
#
#
# class OrderProduct(models.Model):
#     product = models.ForeignKey(Product, related_name="Products", on_delete=models.CASCADE)
#     order = models.ForeignKey(Orders, related_name="orders", on_delete=models.CASCADE)
#     count = models.PositiveIntegerField()
#
#
class CartProduct(models.Model):
    product = models.ForeignKey(Product, related_name="CartProducts", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="Cartuser", on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
#
#
# class Mailing_news(models.Model):
#     email = models.EmailField(verbose_name="email address", blank=True, db_index=True)
