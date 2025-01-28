from django.contrib import admin
from .models import Account, People, Debate, Location, Ticket


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ("ID", "name", "english_level", "phone_number", "created_at")
    search_fields = ("ID", "name", "english_level", "phone_number")
    list_filter = ("english_level",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "debate", "is_used", "created_at")
    search_fields = ("id", "user", "debate")
    list_filter = ("is_used", "debate",)


@admin.register(Debate)
class DebateAdmin(admin.ModelAdmin):
    def number_of_people(self, obj):
        return obj.people.count()

    def b1_b2(self, obj):
        return obj.people.filter(english_level="B1-B2").count()

    def c1_c2(self, obj):
        return obj.people.filter(english_level="C1-C2").count()

    list_display = ("location", "b1_b2", "c1_c2", "number_of_people", "is_expired", "date")
    search_fields = ("name", "location__name")
    list_filter = ("location", "is_expired")


admin.site.register(Account)
admin.site.register(Location)
