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
    tracking=models.CharField(max_length=50,null=True)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.SET_NULL,null=True)
    courier=models.ForeignKey(Courier,on_delete=models.SET_NULL,null=True)
    create=models.DateTimeField(null=True)
    sent=models.DateTimeField(null=True)
    shipping_name=models.CharField(max_length=50,verbose_name="Nome Destinatario")
    shipping_address=models.CharField(max_length=50,verbose_name="Indirizzo destinatario")
    shipping_phone=PhoneNumberField(blank=True,verbose_name="Telefono destinatario")
    shipping_city=models.CharField(max_length=50,verbose_name="Città di destinazione")
    shipping_cap=models.CharField(max_length=5,blank=True,null=True,verbose_name="CAP di destinazione")
    shipping_country=models.CharField(max_length=20,verbose_name="Nazione di destinazione")
    shipping_state=models.CharField(max_length=20,verbose_name="Provincia di destinazione",null=True)

    status=models.CharField(max_length=2,choices=[("N","Nuova"),("C","Creata"),("S","Inviata"),("E","Errore"),("W","Attenzione"),("T","In transito"),("D","Consegnata")],default="N")
    qty=models.PositiveIntegerField(default=1)
    cod=models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
    cod_method=models.CharField(max_length=2,choices=[("C","Contante"),("A","Assegno"),("D","Come consegnata")],blank=True,null=True)
    class Meta:
        verbose_name = "Spedizione"
        verbose_name_plural = "Spedizioni"

    def __str__(self):
        return str(self.shipping_name)+","+str(self.shipping_city)+","+str(self.shipping_country)

class ShippingList(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.SET_NULL,null=True)
    courier=models.ForeignKey(Courier,on_delete=models.SET_NULL,null=True)
    create=models.DateTimeField(default=timezone.now)
    shippings=models.ManyToManyField(Shipping)
