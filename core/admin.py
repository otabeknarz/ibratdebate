from django.contrib import admin
from .models import Account, People, Debate, Location

admin.site.register(Account)
admin.site.register(People)
admin.site.register(Location)
admin.site.register(Debate)
