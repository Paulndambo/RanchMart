from django.db import models
from core.models import AbstractBaseModel

# Create your models here.

class Payment(AbstractBaseModel):
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.order.user.username} - {self.amount}"