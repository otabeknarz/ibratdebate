from django.shortcuts import render
from core.models import Account, Debate, Ticket
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.models import User, Account
from .serializers import DebateSerializer
from core.serializers import TicketResponseSerializer
from users.serializers import (
    AccountIdSerializer,
    AccountCreateSerializer,
    UserResponseSerializer,
    AccountResponseSerializer,
    AccountPatchUpdateSerializer,
)


@api_view(["POST"])
def auth_user(request):
    user = User.objects.filter(id=request.data.get("id")).first()
    if not user:
        serializer = AccountCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    if user.first_name == "" or not user.first_name:
        return Response(
            {
                "registering_is_not_completed": True,
                "what_to_update": "first_name",
                "user": AccountResponseSerializer(user).data
            },
            status=400
        )
    elif user.phone_number == "" or not user.phone_number:
        return Response(
            {
                "registering_is_not_completed": True,
                "what_to_update": "phone_number",
                "user": AccountResponseSerializer(user).data
            },
            status=400
        )
    elif user.english_level == "" or not user.english_level:
        return Response(
            {
                "registering_is_not_completed": True,
                "what_to_update": "english_level",
                "user": AccountResponseSerializer(user).data
            },
            status=400
        )
    elif user.age == "" or not user.age:
        return Response(
            {
                "registering_is_not_completed": True,
                "what_to_update": "age",
                "user": AccountResponseSerializer(user).data
            },
            status=400
        )
    else:
        return Response(AccountResponseSerializer(user).data, status=400)


@api_view(["PATCH"])
def update_user(request, user_id: str):
    user = Account.account.filter(id=user_id).first()
    if not user:
        return Response({"detail": f"No user found with the id {user_id}"}, status=404)
    
    serializer = AccountPatchUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(AccountResponseSerializer(user).data, status=200)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def create_user(request):
    user = User.objects.filter(id=request.data.get("id")).first()
    if user:
        return Response(
            {
                "detail": "The user already exists with the given id",
                "user": UserResponseSerializer(user).data,
            },
            status=400
        )

    serializer = AccountCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(password=serializer.validated_data.get("id"))
        return Response(UserResponseSerializer(user).data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def get_user(request):
    id = request.data.get("id")
    if not id:
        return Response({"detail": "The field id must be filled"}, status=400)

    user = User.objects.filter(id=id).first()
    if not user:
        return Response({"detail": "There is no user with the given id"}, status=400)

    return Response(UserResponseSerializer(user).data, status=200)


@api_view(["GET"])
def get_me(request):
    if not request.user.is_authenticated:   
        return Response({"detail": "You was not authenticated"}, status=401)
    return Response(UserResponseSerializer(request.user).data, status=200)


@api_view(["POST"])
def create_people(request):
    id = request.data.get("ID")
    name = request.data.get("first_name")
    if id is None and name is None:
        return Response(
            {"status": "false", "detail": "id and name is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.filter(id=id).first()

    if user:
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
    account = Account.account.filter(id=request.data.get("user_id")).first()
    debate = Debate.objects.filter(id=request.data.get("debate_id")).first()

    if account and debate:
        ticket = Ticket(debate=debate, user=account)
        ticket.save()
    else:
        return Response({"detail": "We could not find account or debate with the given credentials"}, status=404)

    return Response(TicketResponseSerializer(ticket).data, status=201)
