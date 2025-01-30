from django.db import models
from flight.models import Flight
from cabin.models import Cabin
from user.models import CustomUser
from .choices import BOOKING_STATUS_CHOICES, GENDER_CHOICES, PAYMENT_STATUS_CHOICES, CURRENCY_CHOICES


class BookFlight(models.Model):
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='booked_flights')
    title = models.CharField(max_length=255, blank=True, null=True)
    fullname = models.CharField(max_length=255)
    email = models.EmailField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    phone = models.CharField(max_length=12)
    cabin = models.ForeignKey('cabin.Cabin', on_delete=models.CASCADE)
    flight = models.ForeignKey('flight.Flight', on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    invoice_number = models.CharField(max_length=25)
    booking_status = models.CharField(choices=BOOKING_STATUS_CHOICES, max_length=10, default="pending")
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=20, default='usd')
    booking_id = models.CharField(max_length=7)
    pnr = models.CharField(max_length=7)
    payment_status = models.CharField(choices=PAYMENT_STATUS_CHOICES, max_length=25, default='pending')
    children = models.IntegerField(default=0)
    infants = models.IntegerField(default=0)
    adults = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.adult_price
