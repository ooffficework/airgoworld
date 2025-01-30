from django.db import models
from .choices import METHOD_CHOICES
class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, choices=METHOD_CHOICES, unique=True)
    details = models.JSONField() 
    is_active = models.BooleanField(default=True)   
    display = models.BooleanField(default=False) 
    def __str__(self):
        return self.get_name_display()
