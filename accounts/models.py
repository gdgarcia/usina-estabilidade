from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # using our custom field 'age'
    age = models.PositiveIntegerField(null=True, blank=True)
