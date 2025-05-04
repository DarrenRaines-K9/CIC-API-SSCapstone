from django.db import models
from .volunteer import Volunteer
from .events import Event


class EventVolunteer(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="event_volunteers"
    )
    volunteer = models.ForeignKey(
        Volunteer, on_delete=models.CASCADE, related_name="event_volunteers"
    )
