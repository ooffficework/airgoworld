from django.db import models


class Protect(models.Model):
    email = models.EmailField()
    code  = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)