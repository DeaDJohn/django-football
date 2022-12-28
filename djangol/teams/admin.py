from django.contrib import admin

# Register your models here.
from .models import Team, Country,Player

# Register your models here.
admin.site.register(Team)
admin.site.register(Country)
admin.site.register(Player)
