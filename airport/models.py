from .choices import STATUS_CHOICES, SCOPE_CHOICES
from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    iata = models.CharField(max_length=3, unique=True)
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES)
    active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.iata}), {self.country}"
    class Meta:
        unique_together = ('country', 'city', 'name', 'scope', 'iata')
