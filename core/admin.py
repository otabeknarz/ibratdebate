from django.contrib import admin
from .models import Debate, Location, Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "debate", "is_used", "created_at")
    search_fields = ("id",)
    list_filter = ("is_used", "debate",)


@admin.register(Debate)
class DebateAdmin(admin.ModelAdmin):
    list_display = ("location", "is_expired", "date")
    search_fields = ("name", "location__name")
    list_filter = ("location", "is_expired")

admin.site.register(Location)
