from django.contrib import admin
from .models import useradmin, Crew, Port, Ship
# Register your models here.

admin.site.register(useradmin)
admin.site.register(Crew)
admin.site.register(Port)
admin.site.register(Ship)