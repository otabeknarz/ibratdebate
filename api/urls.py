from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("create-people/", views.create_people),
    path("get-people-id/", views.get_people_id),
    path("check-people/<str:people_id>/", views.check_people),
    path("get-debates/", views.get_debates),
    path("register-people-to-debate/", views.register_people_to_debate),
]
