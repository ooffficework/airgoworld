from .choices import CAR_TYPE_CHOICES, TRANSMISSION_CHOICES
from django.db import models


class Car(models.Model):
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    rental_price = models.IntegerField(default=0)
    speed = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.JSONField(blank=True, null=True)
    available = models.BooleanField(default=True)
    display = models.BooleanField(default=True)
    fuel_type = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    capacity = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} "
