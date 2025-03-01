from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "phone_number", "role", "created_at")
    list_filter = ("role", "role_type")
    search_fields = ("username", "email", "phone_number")
    list_editable = ("role",)
    fieldsets = (
        ("Asosiy ma'lumotlar", {"fields": ("id", "username", "password")}),
        ("Qo'shimcha ma'lumotlar", {"fields": (
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "english_level",
            "age",
            "profile_picture",
            "role",
            "role_type",
            "is_staff",
            "is_superuser",
        )}),
        ("Sanalar", {"fields": ("created_at", "updated_at")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("username", "password1", "password2")}),
    )
    ordering = ("username",)
    filter_horizontal = ()
    readonly_fields = ("id", "password", "created_at", "updated_at")
