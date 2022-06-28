from django.db import models
from companies.models import Company
from backend import globals 
# Create your models here.



    
class Marketplace(models.Model):

    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    country=models.CharField(max_length=2,choices=globals.COUNTRY_CHOICES)
    code=models.CharField(max_length=5,choices=globals.MARKETPLACE_CHOICES)
    status=models.BooleanField(default=False)
    website=models.URLField(blank=True)
    endpoint=models.URLField(blank=True,verbose_name="API URL")
    endpoint_user=models.CharField(max_length=50,blank=True,verbose_name="API USER/TOKEN")
    endpoint_password=models.CharField(max_length=400,blank=True,verbose_name="API_SECRET_KEY")
    
    
    class Meta:
        unique_together = ('company', 'country','code')
        verbose_name = "Marketplace"
        verbose_name_plural = "Marketplaces"

    def __str__(self):
        return ("%s_%s_%s" % (self.company,self.code,self.country))

    

