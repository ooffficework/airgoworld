from django.contrib.auth.models import User
from .choices import STATUS_CHOICES
from django.db import models


class Tour(models.Model):
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    description = models.TextField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    location = models.CharField(max_length=255)
    display = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    name = models.CharField(max_length=255)
    reviews = models.IntegerField()
    images = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
