from .choices import ROOM_TYPE_CHOICES, STATUS_CHOICES
from hotel.models import Hotel
from django.db import models


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms", blank=True, null=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default="single")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(upload_to="rooms/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    bed = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.room_type}) - {self.hotel.name}"
