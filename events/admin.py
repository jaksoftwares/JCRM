from django.contrib import admin
from .models import Event, EventCategory

admin.site.register(EventCategory)
admin.site.register(Event)
