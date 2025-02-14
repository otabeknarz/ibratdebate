import os
import uuid
import qrcode
from users.models import User
from django.db import models
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["created_at"])]


class Location(BaseModel):
    name = models.CharField(max_length=255)
    telegram_group_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Debate(BaseModel):
    name = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="images/news/", null=True, blank=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="debates",
    )
    date = models.DateTimeField()
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.location.name} ({self.date})"

    class Meta:
        ordering = ["-updated_at"]


class Account(BaseModel):
    ID = models.CharField(primary_key=True, unique=True, max_length=40)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_staff_acc = models.BooleanField(default=True)
    role = models.CharField(max_length=300, null=True)
    image = models.ImageField(upload_to="images/accounts/", blank=True, null=True)
    admin_to_location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="accounts",
    )

    def __str__(self):
        return self.user.username


class People(BaseModel):
    class EnglishLevels(models.TextChoices):
        B = "B1-B2", "B1-B2"
        C = "C1-C2", "C1-C2"

    class Ages(models.TextChoices):
        TWELVE = "12-14", "12-14"
        FOURTEEN = "14-16", "14-16"
        SIXTEEN = "16-18", "16-18"
        EIGHTEEN = "18<", "18 va undan yuqori"

    ID = models.CharField(max_length=40, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    english_level = models.CharField(
        max_length=5, null=True, blank=True, choices=EnglishLevels.choices
    )
    phone_number = models.CharField(max_length=40, null=True, blank=True)
    debates = models.ManyToManyField(Debate, related_name="people")

    def __str__(self):
        return self.name


def create_qr_code(id: str) -> str:
    qr_code = qrcode.make(data=id)
    qr_code.save(settings.BASE_DIR / f"media/images/qr_codes/{id}.png")
    return f"images/qr_codes/{id}.png"


class Ticket(BaseModel):
    id = models.UUIDField(max_length=40, primary_key=True, unique=True, default=uuid.uuid4)
    debate = models.ForeignKey(Debate, on_delete=models.CASCADE, related_name="tickets")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    is_used = models.BooleanField(default=False)
    qr_code_path = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate QR code if it hasn't been generated yet
        if not self.qr_code_path:
            self.qr_code_path = create_qr_code(str(self.id))
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.qr_code_path:
            try:
                os.remove(settings.BASE_DIR / f"media/{self.qr_code_path}")
            except Exception as e:
                logger.error(r)
        super().delete(*args, **kwargs)
