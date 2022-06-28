from django.db import models
from marketplaces.models import Marketplace
from companies.models import Company
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class Courier(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    name=models.CharField(max_length=10,choices=[("GLS","GLS"),("BRT","BRT"),("DHL","DHL"),("UPS","UPS"),("SDA","SDA"),("CRONO","Crono Poste")])
    location=models.CharField(max_length=10,blank=True,verbose_name="Sede")
    client=models.CharField(max_length=20,blank=True,verbose_name="Codice cliente")
    password=models.CharField(max_length=20,blank=True,verbose_name="Password Cliente")
    contract=models.CharField(max_length=20,blank=True,verbose_name="Codice Contratto")
    endpoint=models.URLField(blank=True,verbose_name="Endpoint API")
    active=models.BooleanField(default=False)

    class Meta:
        verbose_name = "Corriere"
        verbose_name_plural = "Corrieri"

class Shipping(models.Model):
    tracking=models.CharField(max_length=50)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.SET_NULL,null=True)
    courier=models.ForeignKey(Courier,on_delete=models.SET_NULL,null=True)
    create=models.DateTimeField(default=timezone.now)
    sent=models.DateTimeField(null=True)
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    phone=PhoneNumberField(blank=True)
    city=models.CharField(max_length=50)
    cap=models.CharField(max_length=5,blank=True)
    country=models.CharField(max_length=20)
    status=models.CharField(max_length=2,choices=[("N","Nuova"),("C","Creata"),("S","Inviata"),("E","Errore"),("W","Attenzione"),("T","In transito"),("D","Consegnata")],default="N")
    qty=models.PositiveIntegerField(default=1)
    cod=models.DecimalField(max_digits=6,decimal_places=2,blank=True)
    cod_method=models.CharField(max_length=2,choices=[("C","Contante"),("A","Assegno"),("D","Come consegnata")],blank=True)
    class Meta:
        verbose_name = "Spedizione"
        verbose_name_plural = "Spedizioni"

    def __str__(self):
        return str(self.tracking)+"_"+str(self.name)+"_"+str(self.city)+"_"+str(self.country)

class ShippingList(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.SET_NULL,null=True)
    courier=models.ForeignKey(Courier,on_delete=models.SET_NULL,null=True)
    create=models.DateTimeField(default=timezone.now)
    shippings=models.ManyToManyField(Shipping)
