from django.db import models
from .choices import TRIP_TYPE_CHOICES

class Flight(models.Model):
    origin = models.ForeignKey(
        'airport.Airport', on_delete=models.CASCADE, related_name="flights_origin"
    )
    destination = models.ForeignKey(
        'airport.Airport', on_delete=models.CASCADE, related_name="flights_destination"
    )
    airline = models.ForeignKey(
        'airline.Airline', on_delete=models.CASCADE, related_name="flights"
    )
    flight_number = models.CharField(max_length=10, unique=True)
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    flight_duration = models.DurationField()
    return_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.CharField(max_length=20,blank=True, null=True)
    def __str__(self):
        return f"Flight {self.flight_number}: {self.origin} to {self.destination}"
