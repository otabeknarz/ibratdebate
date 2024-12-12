from django.contrib.auth.models import User
from django.db import models


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
    age = models.CharField(max_length=5, null=True, blank=True, choices=Ages.choices)
    phone_number = models.CharField(max_length=40)
    username = models.CharField(max_length=255, null=True, blank=True)
    debates = models.ManyToManyField(Debate, related_name="people")

    def __str__(self):
        return self.name
