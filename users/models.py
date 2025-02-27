from django.db import models
from django.contrib.auth.models import AbstractUser

from core.models import AbstractBaseModel
from core.constants import USER_ROLE_CHOICES, GENDER_CHOICES


# Create your models here.
class User(AbstractBaseModel, AbstractUser):
    role = models.CharField(max_length=20, default="Customer")
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    county = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    def __str__(self):
        return self.username
    
    def cart_items(self):
        carts = self.carts.cartitems.all().count()
        
        return carts
    
    def name(self):
        return f"{self.first_name} {self.last_name}"
    