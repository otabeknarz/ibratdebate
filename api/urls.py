from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    # users app urls
    path("users/auth/", views.auth_user),
    path("users/update/<str:user_id>/", views.update_user),
    path("users/create/", views.create_user),
    path("users/get-me/", views.get_me),
    path("users/get/", views.get_user),
    # path("update-people/<str:people_id>/", views.update_people),
    path("get-people-id/", views.get_people_id),
    path("check-people/<str:people_id>/", views.check_people),
    path("get-debates/", views.get_debates),
    path("register-people-to-debate/", views.register_people_to_debate),
]
