from django.db import models


class BankInfo(models.Model):
    name = models.CharField(max_length=255)
    header_text = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255, blank=True, null=True)