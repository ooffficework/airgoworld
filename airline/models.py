from .choices import STATUS_CHOICES
from django.db import models


class Airline(models.Model):
    name = models.CharField(max_length=100)
    iata = models.CharField(max_length=3, unique=True)
    country = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    logo = models.CharField(max_length=255,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name}"