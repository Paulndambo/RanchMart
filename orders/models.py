from decimal import Decimal
from django.db import models
from django.db.models import Sum

from core.models import AbstractBaseModel
from shop.models import Animal

# Create your models here.
STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Paid', 'Paid'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
    ('Partially Paid', 'Partially Paid'),
    ('Payment Confirmed', 'Payment Confirmed'),
]
class Cart(AbstractBaseModel):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name='carts')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.total_cost}"
    

class CartItem(AbstractBaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cart.user.username} - {self.animal.name}"
    
    def total_cost(self):
        return self.animal.price * Decimal(self.quantity)


class Order(AbstractBaseModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=100, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    receiver = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='ordersreceiver', null=True, blank=True)
    payment_reference = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    payment_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def remaining_balance(self):
        return self.total_cost - self.amount_paid


class OrderItem(AbstractBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.animal.name
    
    def total_price(self):
        return self.animal.price * Decimal(self.quantity)

