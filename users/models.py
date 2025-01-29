from django.db import models
from django.contrib.auth.models import AbstractUser
import random


def get_random_id() -> str:
    return str(random.randint(10000000, 99999999))


class User(AbstractUser):
    class Role(models.IntegerChoices):
        ADMIN = 1, "Admin"
        COORDINATOR = 2, "Coordinator"
        SELLER = 3, "Seller"
        ACCOUNT = 4, "Account"

    class EnglishLevels(models.TextChoices):
        B = "B1-B2", "B1-B2"
        C = "C1-C2", "C1-C2"

    class Ages(models.TextChoices):
        TWELVE = "12-14", "12-14"
        FOURTEEN = "14-16", "14-16"
        SIXTEEN = "16-18", "16-18"
        EIGHTEEN = "18<", "18 va undan yuqori"

    base_role = Role.ACCOUNT

    id = models.CharField(max_length=40, primary_key=True, default=get_random_id, unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True, unique=True)
    profile_picture = models.ImageField(upload_to="images/profile_pictures/", default="images/default_user.png")
    from_group = models.BooleanField(default=False)
    role = models.IntegerField(choices=Role.choices, default=base_role)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    english_level = models.CharField(max_length=5, null=True, blank=True, choices=EnglishLevels.choices)
    age = models.CharField(max_length=5, null=True, blank=True, choices=Ages.choices)

    groups = None
    user_permissions = None

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.phone_number:
                if "+" in self.phone_number:
                    self.phone_number = self.phone_number.replace("+", "")

        super().save(*args, **kwargs)


class AdminManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.ADMIN)


class Admin(User):
    base_role = User.Role.ADMIN

    admin = AdminManager()

    class Meta:
        proxy = True
        verbose_name = "Admin"
        verbose_name_plural = "Admins"


class CoordinatorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.COORDINATOR)


class Coordinator(User):
    base_role = User.Role.COORDINATOR

    coordinator = CoordinatorManager()

    class Meta:
        proxy = True
        verbose_name = "Coordinator"
        verbose_name_plural = "Coordinators"


class SellerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.SELLER)


class Seller(User):
    base_role = User.Role.SELLER

    seller = SellerManager()

    class Meta:
        proxy = True
        verbose_name = "Seller"
        verbose_name_plural = "Sellers"


class AccountManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.ACCOUNT)


class Account(User):
    base_role = User.Role.ACCOUNT

    account = AccountManager()

    class Meta:
        proxy = True
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
