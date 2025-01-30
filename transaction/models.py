from .choices import PAYMENT_GATEWAY_CHOICES, TRANSACTION_TYPE_CHOICES
from django.contrib.auth.models import User
from django.db import models


class Transaction(models.Model):
    payment_gateway = models.CharField(max_length=50, choices=PAYMENT_GATEWAY_CHOICES)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trx_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255)
    currency = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.type} transaction of {self.amount} {self.currency} by {self.user.username}"

    class Meta:
        ordering = ["-created_at"]
