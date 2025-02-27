from django.db import models

from core.models import AbstractBaseModel
# Create your models here.
ANIMAL_TYPE = (
    ('Beef', 'Beef'),
    ('Dairy', 'Dairy'),
)

class Category(AbstractBaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Animal(AbstractBaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='animals/', null=True, blank=True)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=255, null=True, blank=True)
    species = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    medical_certificate = models.FileField(upload_to='medical_certificates/', null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    animal_type = models.CharField(max_length=255, choices=ANIMAL_TYPE, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class AnimalImage(AbstractBaseModel):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='animals/')

    def __str__(self):
        return f"{self.animal.name} - {self.id}"