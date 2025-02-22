from rest_framework import serializers
from .models import Ticket, Debate, Location


class TicketResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "user",
            "debate",
            "is_used",
            "qr_code_path",
            "created_at",
        )


class LocationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "name", "telegram_group_link")


class DebateResponseSerializer(serializers.ModelSerializer):
    location = LocationResponseSerializer()
    class Meta:
        model = Debate
        fields = (
            "id",
            "location",
            "date",
            "is_expired",
        )
