from django.db import models


class Location(models.Model):

    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()
