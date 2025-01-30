from django.db import models
from .choices import CABIN_CHOICES

class Cabin(models.Model):
    name = models.CharField(choices=CABIN_CHOICES, max_length=20)
    flight = models.ForeignKey('flight.Flight', on_delete=models.CASCADE, related_name='cabin')
    prices = models.JSONField(dict)
    amenities = models.JSONField()
    
    def __str__(self):
        return self.name    