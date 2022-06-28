from django.db import models
from companies.models import Company
from marketplaces.models import Marketplace
from django.utils import timezone
from backend import globals
from shippings.models import Shipping
from customers.models import Customer
# Create your models here.


class OrderDetail(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH)
    qty=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=8,decimal_places=2)
    iva=models.DecimalField(max_digits=8,decimal_places=2)
    shipping_price=models.DecimalField(max_digits=8,decimal_places=2)
    shipping_iva=models.DecimalField(max_digits=8,decimal_places=2)
    

class Order(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    order_id=models.CharField(max_length=50)
    date=models.DateTimeField(default=timezone.now)
    detail=models.ManyToManyField(OrderDetail)
    status=models.CharField(max_length=2,choices=globals.ORDER_STATUS_CHOICES)
    shipping=models.ForeignKey(Shipping,on_delete=models.SET_NULL,null=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)