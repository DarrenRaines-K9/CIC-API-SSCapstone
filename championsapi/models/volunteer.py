from django.db import models
from django.contrib.auth.models import User


class Volunteer(models.Model):

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=55)
    phone_number = models.CharField(max_length=55)
