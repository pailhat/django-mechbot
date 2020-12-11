from django.contrib import admin

# Register your models here.
from .models import DiscordUser, Alert

admin.site.register(DiscordUser)
admin.site.register(Alert)