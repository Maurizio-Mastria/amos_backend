from django.db import models
from buckets.models import Bucket
from companies.models import Company
from marketplaces.models import Marketplace
from django.utils import timezone
from django.conf import settings
# Create your models here.
class Import(models.Model):

    path=models.CharField(max_length=200)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    filename=models.CharField(max_length=200)
    marketplace=models.ManyToManyField(Marketplace)
    create=models.DateTimeField(default=timezone.now)
    ftype=models.CharField(max_length=10,choices=[("products","Prodotti"),("orders","Ordini"),("prices","Prezzi"),("qty","Quantità")])
    status=models.CharField(max_length=2,choices=[("N","Nuovo"),("C","Configurazione"),("W","In attesa di elaborazione"),("P","In elaborazione"),("E","Errore"),("D","Elaborato")],default="N")
    datasheet=models.JSONField(blank=True,null=True)
    messages=models.JSONField(blank=True,null=True)
    