from django.db import models

class Hotel(models.Model):
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0) 
    price_per_night = models.DecimalField(decimal_places=2, max_digits=10)
    parking = models.BooleanField(default=False)
    images = models.JSONField(blank=True, null=True)
    restaurant = models.BooleanField(default=True)
    available = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    casino = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255)
    pool = models.BooleanField(default=False)
    spa = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    bar = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
   