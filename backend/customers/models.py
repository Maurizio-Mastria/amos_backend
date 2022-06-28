from django.db import models
from backend import globals
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=80)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    cap=models.CharField(max_length=5,blank=True)
    phone=PhoneNumberField(blank=True)
    country=models.CharField(max_length=2,choices=globals.COUNTRY_CHOICES)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"

    def __str__(self):
        return str(self.name)