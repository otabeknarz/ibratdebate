from django.contrib import admin
from .models import Account, People, Debate, Location


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('ID', 'name', 'english_level', 'phone_number')
    search_fields = ('ID', 'name', 'english_level', 'phone_number')
    list_filter = ('name', 'english_level', 'phone_number')


admin.site.register(Account)
admin.site.register(People)
admin.site.register(Location)
admin.site.register(Debate)
