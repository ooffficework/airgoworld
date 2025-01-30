from django.db import models
from .choices import COUNTRY_STATUS_CHOICES


class Country(models.Model):
    country_status = models.CharField(
        max_length=20, choices=COUNTRY_STATUS_CHOICES, default="active"
    )
    num_code = models.CharField(max_length=3, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    iso3 = models.CharField(max_length=3, unique=True)
    iso = models.CharField(max_length=2, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_code = models.CharField(max_length=5)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
