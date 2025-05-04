from django.db import models
from .volunteer import Volunteer


class Inventory(models.Model):
    volunteer = models.ForeignKey(
        Volunteer, on_delete=models.DO_NOTHING, related_name="inventory"
    )
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
