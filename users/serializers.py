from rest_framework import serializers
from .models import User, Account


class AccountIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id",)


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "profile_picture",
            "phone_number",
            "english_level",
            "age",
        )
        extra_kwargs = {
            "id": {"required": True},
            "username": {"required": True}
        }

class AccountPatchUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "first_name",
            "username",
            "phone_number",
            "english_level",
            "age",
        )


class AccountResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "profile_picture",
            "phone_number",
            "english_level",
            "age",
        )


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "profile_picture",
            "phone_number",
            "english_level",
            "age",
            "role",
            "created_at",
        )
