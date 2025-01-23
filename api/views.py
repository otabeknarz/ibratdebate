from django.shortcuts import render
from core.models import People, Account, Debate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.models import User, Admin, Coordinator, Seller, Account
from .serializers import DebateSerializer
from users.serializers import AccountIdSerializer, AccountCreateSerializer, UserResponseSerializer


@api_view(["POST"])
def create_people(request):
    id = request.data.get("ID")
    name = request.data.get("first_name")
    if id is None and name is None:
        return Response(
            {"status": "false", "detail": "id and name is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.filter(id=id)

    if user.exists():
        return Response(
            {
                "status": "false",
                "detail": "User with this id already exists",
                "people": UserResponseSerializer(user.first()).data
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = AccountCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"status": "false", "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


# @api_view(["POST"])
# def update_people(request, people_id):
#     try:
#         people = People.objects.get(ID=people_id)
#         people.name = request.data.get("name", people.name)
#         people.english_level = request.data.get("english_level", people.english_level)
#         people.phone_number = request.data.get("phone_number", people.phone_number)
#         people.save()
#         serializer = PeopleSerializer(people)
#     except Exception as e:
#         return Response(
#             {"status": "false", "detail": str(e)},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )
#     return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def check_people(request, id):
    try:
        account = Account.account.get(id=id)
        serializer = UserResponseSerializer(account)
    except Exception as e:
        return Response(
            {"status": "false", "detail": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if account.phone_number is None:
        return Response(
            {"status": "false", "detail": "Account has not been registered yet"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(
        {"status": "true", "people": serializer.data}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def get_people_id(request):
    account_serializer = AccountIdSerializer(Account.account.all(), many=True)
    return Response({"status": "true", "people_ID": account_serializer.data})


@api_view(["GET"])
def get_debates(request):
    debates = Debate.objects.filter(is_expired=False)
    serializer = DebateSerializer(debates, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def register_people_to_debate(request):
    try:
        account = Account.account.get(id=request.data["people_id"])
        debate = Debate.objects.get(pk=request.data["debate_id"])

        account.debates.add(debate)
        account.save()
        account_serializer = UserResponseSerializer(account)
        debate_serializer = DebateSerializer(debate)

    except Exception as e:
        return Response(
            {"status": "false", "detail": str(e)},
        )

    return Response(
        {
            "status": "true",
            "people": account_serializer.data,
            "debate": debate_serializer.data,
        },
        status=status.HTTP_201_CREATED,
    )
