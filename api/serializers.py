from core.models import People, Account, Debate, Location
from rest_framework import serializers


class PeopleIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ("ID",)


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = "ID", "name", "english_level", "phone_number", "debates"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "name", "telegram_group_link"


class DebateSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Debate
        fields = "pk", "date", "location"
