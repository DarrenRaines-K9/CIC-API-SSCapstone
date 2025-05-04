from django.contrib import admin
from .models import Volunteer, EventVolunteer, Location, Event, Inventory

# Register your models here.
admin.site.register(Volunteer)
admin.site.register(EventVolunteer)
admin.site.register(Location)
admin.site.register(Event)
admin.site.register(Inventory)
