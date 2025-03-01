from django.urls import path
from . import views

app_name = "core"
#
urlpatterns = [
    path("404", views.error_404, name="home"),
#     path("purpose/", views.purpose, name="purpose"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
#     path(
#         "previous_debate/<int:debate_id>/",
#         views.previous_debate,
#         name="previous_debate",
#     ),
#     path("team/", views.team_view, name="team"),
#     path("previous_debates/", views.previous_debates_view, name="previous_debates"),
    path("stats/", views.stats, name="stats"),
     path("", views.qr_code_scanner_view, name="qr_code_scanner"),
]
