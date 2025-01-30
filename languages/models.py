from .choice import STATUS_CHOICES, TYPE_CHOICES
from django.db import models


class Language(models.Model):
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="primary")
    flag = models.ImageField(upload_to="languages/flags/", null=True, blank=True)
    language_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.language_code} - {self.country}"
