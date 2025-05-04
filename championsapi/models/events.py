from django.db import models
from .volunteer import Volunteer
from django.contrib.auth.models import User


class Event(models.Model):
    volunteer = models.ForeignKey(
        Volunteer, on_delete=models.DO_NOTHING, related_name="volunteer"
    )
    title = models.CharField(max_length=255)
    location = models.ForeignKey(
        "Location", on_delete=models.DO_NOTHING, related_name="location"
    )
    volunteers = models.ManyToManyField(
        Volunteer, through="EventVolunteer", related_name="event"
    )
    time = models.TimeField()
    date = models.DateField()
