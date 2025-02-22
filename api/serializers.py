from core.models import Debate, Location
from rest_framework import serializers
from users.models import User


class UsersIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",)
