from rest_framework import serializers
from .models import User, Admin, Coordinator, Seller, Account


class AccountIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id",)


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "first_name",
            "last_name",
            "profile_picture",
            "phone_number",
            "age",
            "english_level"
        )


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "profile_picture",
            "phone_number",
            "age",
            "english_level",
            "role",
        )
