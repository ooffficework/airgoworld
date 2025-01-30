from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.db import models
from .choices import GENDER_CHOICES

class HotelBooking(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)
    hotel = models.ForeignKey('hotel.Hotel', on_delete=models.CASCADE)
    fullname = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    booked_at = models.DateTimeField(auto_now_add=True)
    display = models.BooleanField(default=True)
    check_out_date = models.DateTimeField()
    check_in_date = models.DateTimeField()
    occupants = models.IntegerField()
    no_of_rooms = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.total_bill

    
