from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "phone_number", "role", "from_group", "created_at")
    list_filter = ("role", "from_group")
    search_fields = ("username", "email", "phone_number")
    list_editable = ("role", "from_group")
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
            "from_group",
        )}),
        ("Sanalar", {"fields": ("created_at", "updated_at")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("username", "password1", "password2")}),
    )
    ordering = ("username",)
    filter_horizontal = ()
    readonly_fields = ("id", "password", "created_at", "updated_at")
