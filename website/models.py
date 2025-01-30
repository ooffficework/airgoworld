from django.db import models

class Website(models.Model):
    name = models.CharField(max_length=255)
    logo_1 = models.CharField(max_length=255, blank=True, null=True)
    logo_2 = models.CharField(max_length=255, blank=True, null=True)
    logo_3 = models.CharField(max_length=255, blank=True, null=True)
    