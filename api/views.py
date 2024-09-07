from django.shortcuts import render
from core.models import People, Account, Debate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PeopleSerializer, DebateSerializer, PeopleIDSerializer


@api_view(["POST"])
def create_people(request):
    ID = request.data["ID"]
    name = request.data["name"]
    phone_number = request.data["phone_number"]

    try:
        people = People.objects.create(ID=ID, name=name, phone_number=phone_number)
        serializer = PeopleSerializer(people)
    except Exception as e:
        return Response(
            {"status": "false", "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response(
        {"status": "true", "people": serializer.data}, status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
def check_people(request, people_id):
    try:
        people = People.objects.get(ID=people_id)
        serializer = PeopleSerializer(people)
    except Exception as e:
        return Response(
            {"status": "false", "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response(
        {"status": "true", "people": serializer.data}, status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
def get_people_id(request):
    people_serializer = PeopleIDSerializer(People.objects.all(), many=True)
    return Response({"status": "true", "people_ID": people_serializer.data})


@api_view(["GET"])
def get_debates(request):
    debates = Debate.objects.filter(is_expired=False)
    serializer = DebateSerializer(debates, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def register_people_to_debate(request):
    try:
        people = People.objects.get(ID=request.data["people_id"])
        debate = Debate.objects.get(pk=request.data["debate_id"])

        people.debates.add(debate)
        people.save()
        people_serializer = PeopleSerializer(people)
        debate_serializer = DebateSerializer(debate)

    except Exception as e:
        return Response({"status": "false", "detail": str(e)},)

    return Response(
        {
            "status": "true",
            "people": people_serializer.data,
            "debate": debate_serializer.data,
        },
        status=status.HTTP_201_CREATED,
    )
