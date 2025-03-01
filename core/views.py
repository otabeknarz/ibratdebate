import random

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.timezone import localtime
import uuid

from .models import Debate, Ticket, User


# def home(request):
#     accounts = random.choices(
#         list(Account.objects.all()),
#         k=10 if len(Account.objects.all()) > 10 else len(Account.objects.all()),
#     )
#     upcoming_debates = Debate.objects.filter(is_expired=False)[:10]
#     previous_debates = Debate.objects.filter(is_expired=True)[:10]
#     return render(
#         request,
#         "home.html",
#         {
#             "accounts": accounts,
#             "upcoming_debates": upcoming_debates,
#             "previous_debates": previous_debates,
#         },
#     )
#
#
# def previous_debates_view(request):
#     previous_debates = Debate.objects.filter(is_expired=True)
#     return render(
#         request, "previous_debates.html", {"previous_debates": previous_debates}
#     )
#
#
# def purpose(request):
#     return render(request, "purpose.html")
#
#
# def previous_debate(request, debate_id):
#     try:
#         previous_debate_obj = Debate.objects.get(id=debate_id)
#     except Exception as e:
#         return HttpResponse("Debate not found: ", str(e))
#     return render(
#         request, "previous_debate.html", {"previous_debate": previous_debate_obj}
#     )
#
#
# def team_view(request):
#     team_members = Account.objects.all()
#     return render(request, "team.html", {"team_members": team_members})
#
#
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = get_user_model().objects.filter(username=username).first()

        if not user:
            return redirect("core:login")

        if user.check_password(password):
            login(request, user=user)
            return redirect("core:home")
        else:
            return redirect("core:login")

    return render(request, "auth/login.html")


@login_required(login_url="core:login")
def logout_view(request):
    logout(request)
    return redirect("core:login")


def stats(request):
    debates = Debate.objects.filter(is_expired=False)
    data = []
    for debate in debates:
        data.append(
            [
                debate,
                debate.people.all().count(),
                localtime(debate.date).strftime("%d/%m/%Y | %H:%M"),
            ]
        )
    return render(request, "stats.html", {"data": data})


def qr_code_scanner_view(request):
    if request.method == "POST" and request.user.is_authenticated:
        if request.user.role not in (1, 3):
            return redirect("core:home")
        qr_code_data = request.POST.get("qr_code_data")

        try:
            uuid.UUID(qr_code_data, version=4)
        except ValueError:
            return render(request, "qr_code_scanner.html", {"error": True, "error_message": "Invalid QR code"})

        ticket = Ticket.objects.filter(id=qr_code_data).first()
        if not ticket:
            return render(request, "qr_code_scanner.html", {"error": True, "error_message": "Ticket not found"})
        if ticket.is_used:
            return render(request, "qr_code_scanner.html", {"error": True, "error_message": "Ticket already used"})
        ticket.is_used = True
        ticket.save()
        Ticket.objects.filter(user=ticket.user, is_used=False).delete()
        return render(request, "qr_code_scanner.html", {"success": True, "ticket": ticket, "debater": ticket.user})

    if not request.user.is_authenticated:
        return render(request, "auth/login.html")
    elif request.user.role in (1, 2):
        return render(request, "qr_code_scanner.html")
    else:
        return redirect("core:home")


def error_404(request):
    return HttpResponse("<h1>404</h1>", content_type="text/html")