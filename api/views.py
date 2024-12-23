from django.shortcuts import render
from core.models import People, Account, Debate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PeopleSerializer, DebateSerializer, PeopleIDSerializer


@api_view(["POST"])
def create_people(request):
    ID = request.data.get("ID")
    name = request.data.get("name")
    if ID is None and name is None:
        return Response(
            {"status": "false", "detail": "ID and name is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    people = People.objects.filter(ID=ID)

    if people.exists():
        return Response(
            {
                "status": "false",
                "detail": "People with this ID already exists",
                "people": PeopleSerializer(people.first()).data
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = PeopleSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"status": "false", "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def update_people(request, people_id):
    try:
        people = People.objects.get(ID=people_id)
        people.name = request.data.get("name", people.name)
        people.english_level = request.data.get("english_level", people.english_level)
        people.phone_number = request.data.get("phone_number", people.phone_number)
        people.save()
        serializer = PeopleSerializer(people)
    except Exception as e:
        return Response(
            {"status": "false", "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response(serializer.data, status=status.HTTP_200_OK)


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
    if people.phone_number is None:
        return Response(
            {"status": "false", "detail": "People has not been registered yet"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(
        {"status": "true", "people": serializer.data}, status=status.HTTP_200_OK
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
        return Response(
            {"status": "false", "detail": str(e)},
        )

    return Response(
        {
            "status": "true",
            "people": people_serializer.data,
            "debate": debate_serializer.data,
        },
        status=status.HTTP_201_CREATED,
    )
