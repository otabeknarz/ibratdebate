from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

from .models import Account, People, Debate


def home(request):
    accounts = Account.objects.all()[:10]
    upcoming_debates = Debate.objects.filter(is_expired=False)
    previous_debates = Debate.objects.filter(is_expired=True)
    return render(
        request,
        "home.html",
        {"accounts": accounts, "upcoming_debates": upcoming_debates, "previous_debates": previous_debates},
    )


def purpose(request):
    return render(request, "purpose.html")


def previous_debate(request, debate_id):
    try:
        previous_debate_obj = Debate.objects.get(id=debate_id)
    except Exception as e:
        return HttpResponse("Debate not found: ", str(e))
    return render(request, "previous_debate.html", {"previous_debate": previous_debate_obj})


def team_view(request):
    team_members = Account.objects.all()
    return render(request, "team.html", {"team_members": team_members})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user=user)
                return redirect("core:home")
            else:
                return redirect("core:login")

        except User.DoesNotExist:
            return redirect("core:login")

    return render(request, "auth/login.html")


@login_required(login_url="core:login")
def logout_view(request):
    logout(request)
    return redirect("core:login")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        role = request.POST["role"]
        image = request.FILES["image"]
        fs = FileSystemStorage()

        # # save the image on MEDIA_ROOT folder
        # file_name = fs.save(username+"."+image.name.split(".")[-1], image)

        try:
            user = User.objects.create(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            Account.objects.create(user=user, role=role, image=image)
        except Exception as error:
            return HttpResponse(error)

        return redirect("core:home")

    return render(request, "auth/register.html")
