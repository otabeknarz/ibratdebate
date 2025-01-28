from rest_framework import serializers
from .models import Ticket, Debate


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
