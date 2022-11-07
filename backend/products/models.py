from django.db import models
from companies.models import Company
from marketplaces.models import Marketplace
from backend import globals
# Create your models here.

class CustomAttribute(models.Model):
    name=models.CharField(max_length=30)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    description=models.CharField(max_length=30)
    type=models.CharField(max_length=10,choices=[("INT","Intero"),("TEXT","Testo"),("BOOLEAN","Booleano"),("DECIMAL","Decimale"),("URL","Url"),("CHAR","Caratteri")])
    class Meta:
        unique_together = ('name','company')
    def __str__(self):
        return str(self.name)

class DefaultAttribute(models.Model):
    name=models.CharField(max_length=30,unique=True)
    description=models.CharField(max_length=30)
    type=models.CharField(max_length=10,choices=[("INT","Intero"),("TEXT","Testo"),("BOOLEAN","Booleano"),("DECIMAL","Decimale"),("URL","Url"),("CHAR","Caratteri")])
    def __str__(self):
        return str(self.name)

class Attribute(models.Model):
    name=models.CharField(max_length=30,unique=True)
    description=models.CharField(max_length=30)
    type=models.CharField(max_length=10,choices=[("INT","Intero"),("TEXT","Testo"),("BOOLEAN","Booleano"),("DECIMAL","Decimale"),("URL","Url"),("CHAR","Caratteri")])
    def __str__(self):
        return str(self.name)

class Variation(models.Model):
    attribute=models.ForeignKey(Attribute,on_delete=models.CASCADE,default=None)
    def __str__(self):
        return str(self.attribute)


class ProductBooleanEav(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    attribute=models.CharField(max_length=30)
    value=models.BooleanField(default=False)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('company','attribute','marketplace','sku')
    def __str__(self):
        return str(self.company.vid)+"_"+str(self.sku)+"_"+str(self.attribute)

class ProductIntEav(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    attribute=models.CharField(max_length=30)
    value=models.IntegerField()
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('company','attribute','marketplace','sku')
    def __str__(self):
        return str(self.company.vid)+"_"+str(self.sku)+"_"+str(self.attribute)

class ProductDecimalEav(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    attribute=models.CharField(max_length=30)
    value=models.DecimalField(max_digits=6,decimal_places=2)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('company','attribute','marketplace','sku')
    def __str__(self):
        return str(self.company.vid)+"_"+str(self.sku)+"_"+str(self.attribute)
        
class ProductCharEav(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    attribute=models.CharField(max_length=30)
    value=models.CharField(max_length=150)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('company','attribute','marketplace','sku')
    def __str__(self):
        return str(self.company.vid)+"_"+str(self.sku)+"_"+str(self.attribute)

class ProductTextEav(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    attribute=models.CharField(max_length=30)
    value=models.TextField()
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('company','attribute','marketplace','sku')
    def __str__(self):
        return str(self.company.vid)+"_"+str(self.sku)+"_"+str(self.attribute)

class ProductUrlEav(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    attribute=models.CharField(max_length=30)
    value=models.URLField()
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('company','attribute','marketplace','sku')
    def __str__(self):
        return str(self.company.vid)+"_"+str(self.sku)+"_"+str(self.attribute)



class Category(models.Model):
    name=models.CharField(max_length=50)
    title=models.CharField(max_length=100)
    custom_attributes=models.ManyToManyField(CustomAttribute,blank=True)
    attributes=models.ManyToManyField(Attribute,blank=True)
    variations=models.ManyToManyField(Variation,blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,related_name='children')
    marketplace = models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
   
    class Meta:
        unique_together = ('company','name','marketplace')
    def __str__(self):
        return str(self.company)+"_"+str(self.marketplace)+"_"+str(self.title)

class ProductSimple(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH,verbose_name="SKU")
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    gtin=models.CharField(max_length=globals.GTIN_LENGTH,blank=True,verbose_name="GTIN")
    gtin_type=models.CharField(max_length=6,choices=globals.GTIN_CHOICES,default="NOGTIN",verbose_name="Tipo GTIN")
    int_eav=models.ManyToManyField(ProductIntEav,blank=True)
    char_eav=models.ManyToManyField(ProductCharEav,blank=True)
    text_eav=models.ManyToManyField(ProductTextEav,blank=True)
    decimal_eav=models.ManyToManyField(ProductDecimalEav,blank=True)
    boolean_eav=models.ManyToManyField(ProductBooleanEav,blank=True)
    url_eav=models.ManyToManyField(ProductUrlEav,blank=True)
    categories=models.ManyToManyField(Category,blank=True)

    class Meta:
        unique_together = ('sku','company')
    def delete(self,*args,**kwargs):
        for eav in self.int_eav.all():
            eav.delete()
        for eav in self.decimal_eav.all():
            eav.delete()
        for eav in self.char_eav.all():
            eav.delete()
        for eav in self.boolean_eav.all():
            eav.delete()
        for eav in self.text_eav.all():
            eav.delete()
        for eav in self.url_eav.all():
            eav.delete()
        super(ProductSimple,self).delete(*args,**kwargs)
    def __str__(self):
        return str(self.company.vid)+"_"+str(self.sku)


class BulkProductQty(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    bulk_sku=models.CharField(max_length=globals.SKU_LENGTH,verbose_name="SKU")
    product=models.ForeignKey(ProductSimple,on_delete=models.CASCADE)
    qty=models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('company','bulk_sku','product')

class ProductBulk(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH,verbose_name="SKU")
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    bulk_products_qty=models.ManyToManyField(BulkProductQty)
    gtin=models.CharField(max_length=globals.GTIN_LENGTH,blank=True,verbose_name="GTIN")
    gtin_type=models.CharField(max_length=6,choices=globals.GTIN_CHOICES,default="NOGTIN",verbose_name="Tipo GTIN")
    int_eav=models.ManyToManyField(ProductIntEav,blank=True)
    char_eav=models.ManyToManyField(ProductCharEav,blank=True)
    text_eav=models.ManyToManyField(ProductTextEav,blank=True)
    decimal_eav=models.ManyToManyField(ProductDecimalEav,blank=True)
    boolean_eav=models.ManyToManyField(ProductBooleanEav,blank=True)
    url_eav=models.ManyToManyField(ProductUrlEav,blank=True)
    categories=models.ManyToManyField(Category,blank=True)
    class Meta:
        unique_together = ('sku','company')

    def delete(self,*args,**kwargs):
        for eav in self.int_eav.all():
            eav.delete()
        for eav in self.decimal_eav.all():
            eav.delete()
        for eav in self.char_eav.all():
            eav.delete()
        for eav in self.boolean_eav.all():
            eav.delete()
        for eav in self.text_eav.all():
            eav.delete()
        for eav in self.url_eav.all():
            eav.delete()
        for bpq in self.bulk_products_qty.all():
            bpq.delete()
        super(ProductBulk,self).delete(*args,**kwargs)
    def __str__(self):
        return str(self.company.vid)+"_"+str(self.sku)

class ProductMultiple(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH,verbose_name="SKU")
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    product=models.ForeignKey(ProductSimple,on_delete=models.CASCADE)
    qty=models.PositiveIntegerField(default=2)
    gtin=models.CharField(max_length=globals.GTIN_LENGTH,blank=True,verbose_name="GTIN")
    gtin_type=models.CharField(max_length=6,choices=globals.GTIN_CHOICES,default="NOGTIN",verbose_name="Tipo GTIN")
    int_eav=models.ManyToManyField(ProductIntEav,blank=True)
    char_eav=models.ManyToManyField(ProductCharEav,blank=True)
    text_eav=models.ManyToManyField(ProductTextEav,blank=True)
    decimal_eav=models.ManyToManyField(ProductDecimalEav,blank=True)
    boolean_eav=models.ManyToManyField(ProductBooleanEav,blank=True)
    url_eav=models.ManyToManyField(ProductUrlEav,blank=True)
    class Meta:
        unique_together = ('sku','company')
    def delete(self,*args,**kwargs):
        for eav in self.int_eav.all():
            eav.delete()
        for eav in self.decimal_eav.all():
            eav.delete()
        for eav in self.char_eav.all():
            eav.delete()
        for eav in self.boolean_eav.all():
            eav.delete()
        for eav in self.text_eav.all():
            eav.delete()
        for eav in self.url_eav.all():
            eav.delete()
        super(ProductMultiple,self).delete(*args,**kwargs)

    def __str__(self):
        return str(self.company.vid)+"_"+str(self.sku)
        
class ProductConfigurable(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    products=models.ManyToManyField(ProductSimple)
    variations=models.TextField()
    int_eav=models.ManyToManyField(ProductIntEav,blank=True)
    char_eav=models.ManyToManyField(ProductCharEav,blank=True)
    text_eav=models.ManyToManyField(ProductTextEav,blank=True)
    decimal_eav=models.ManyToManyField(ProductDecimalEav,blank=True)
    boolean_eav=models.ManyToManyField(ProductBooleanEav,blank=True)
    url_eav=models.ManyToManyField(ProductUrlEav,blank=True)
    class Meta:
        unique_together = ('sku','company')
    def __str__(self):
        return str(self.company.vid)+"_"+str(self.sku)
    def delete(self,*args,**kwargs):
        for eav in self.int_eav.all():
            eav.delete()
        for eav in self.decimal_eav.all():
            eav.delete()
        for eav in self.char_eav.all():
            eav.delete()
        for eav in self.boolean_eav.all():
            eav.delete()
        for eav in self.text_eav.all():
            eav.delete()
        for eav in self.url_eav.all():
            eav.delete()
        super(ProductConfigurable,self).delete(*args,**kwargs)



# class ProductBulkOfBulk(models.Model):
#     sku=models.CharField(max_length=globals.SKU_LENGTH)
#     company=models.ForeignKey(Company,on_delete=models.CASCADE)
#     gtin=models.CharField(max_length=globals.GTIN_LENGTH,blank=True)
#     gtin_type=models.CharField(max_length=6,choices=globals.GTIN_CHOICES,default="NOGTIN")
#     products=models.ManyToManyField(ProductBulk)
#     int_eav=models.ManyToManyField(ProductIntEav,blank=True)
#     char_eav=models.ManyToManyField(ProductCharEav,blank=True)
#     text_eav=models.ManyToManyField(ProductTextEav,blank=True)
#     decimal_eav=models.ManyToManyField(ProductDecimalEav,blank=True)
#     boolean_eav=models.ManyToManyField(ProductBooleanEav,blank=True)
#     url_eav=models.ManyToManyField(ProductUrlEav,blank=True)
#     class Meta:
#         unique_together = ('sku','company')
    
#     def __str__(self):
#         return str(self.company.vid)+"_"+str(self.sku)


# class ProductBulkOfMultiple(models.Model):
#     sku=models.CharField(max_length=globals.SKU_LENGTH)
#     company=models.ForeignKey(Company,on_delete=models.CASCADE)
#     gtin=models.CharField(max_length=globals.GTIN_LENGTH,blank=True)
#     gtin_type=models.CharField(max_length=6,choices=globals.GTIN_CHOICES,default="NOGTIN")
#     products=models.ManyToManyField(ProductMultiple)
#     int_eav=models.ManyToManyField(ProductIntEav,blank=True)
#     char_eav=models.ManyToManyField(ProductCharEav,blank=True)
#     text_eav=models.ManyToManyField(ProductTextEav,blank=True)
#     decimal_eav=models.ManyToManyField(ProductDecimalEav,blank=True)
#     boolean_eav=models.ManyToManyField(ProductBooleanEav,blank=True)
#     url_eav=models.ManyToManyField(ProductUrlEav,blank=True)
#     class Meta:
#         unique_together = ('sku','company')
    
#     def __str__(self):
#         return str(self.company.vid)+"_"+str(self.sku)

# class ProductMultipleOfBulk(models.Model):
#     sku=models.CharField(max_length=globals.SKU_LENGTH)
#     company=models.ForeignKey(Company,on_delete=models.CASCADE)
#     gtin=models.CharField(max_length=globals.GTIN_LENGTH,blank=True)
#     gtin_type=models.CharField(max_length=6,choices=globals.GTIN_CHOICES,default="NOGTIN")
#     qty=models.IntegerField()
#     product=models.ForeignKey(ProductBulk,on_delete=models.CASCADE)
#     int_eav=models.ManyToManyField(ProductIntEav,blank=True)
#     char_eav=models.ManyToManyField(ProductCharEav,blank=True)
#     text_eav=models.ManyToManyField(ProductTextEav,blank=True)
#     decimal_eav=models.ManyToManyField(ProductDecimalEav,blank=True)
#     boolean_eav=models.ManyToManyField(ProductBooleanEav,blank=True)
#     url_eav=models.ManyToManyField(ProductUrlEav,blank=True)
#     class Meta:
#         unique_together = ('sku','company')
    
#     def __str__(self):
#         return str(self.company.vid)+"_"+str(self.sku)


# class ProductMultipleOfMultiple(models.Model):
#     sku=models.CharField(max_length=globals.SKU_LENGTH)
#     company=models.ForeignKey(Company,on_delete=models.CASCADE)
#     gtin=models.CharField(max_length=globals.GTIN_LENGTH,blank=True)
#     gtin_type=models.CharField(max_length=6,choices=globals.GTIN_CHOICES,default="NOGTIN")
#     qty=models.IntegerField()
#     product=models.ForeignKey(ProductMultiple,on_delete=models.CASCADE)
#     int_eav=models.ManyToManyField(ProductIntEav,blank=True)
#     char_eav=models.ManyToManyField(ProductCharEav,blank=True)
#     text_eav=models.ManyToManyField(ProductTextEav,blank=True)
#     decimal_eav=models.ManyToManyField(ProductDecimalEav,blank=True)
#     boolean_eav=models.ManyToManyField(ProductBooleanEav,blank=True)
#     url_eav=models.ManyToManyField(ProductUrlEav,blank=True)
#     class Meta:
#         unique_together = ('sku','company')
    
#     def __str__(self):
#         return str(self.company.vid)+"_"+str(self.sku)

# class ProductConfigurableOfBulk(models.Model):
#     sku=models.CharField(max_length=globals.SKU_LENGTH)
#     company=models.ForeignKey(Company,on_delete=models.CASCADE)
#     products=models.ManyToManyField(ProductBulk)
#     variations=models.TextField()
#     int_eav=models.ManyToManyField(ProductIntEav,blank=True)
#     char_eav=models.ManyToManyField(ProductCharEav,blank=True)
#     text_eav=models.ManyToManyField(ProductTextEav,blank=True)
#     decimal_eav=models.ManyToManyField(ProductDecimalEav,blank=True)
#     boolean_eav=models.ManyToManyField(ProductBooleanEav,blank=True)
#     url_eav=models.ManyToManyField(ProductUrlEav,blank=True)
#     class Meta:
#         unique_together = ('sku','company')
    
#     def __str__(self):
#         return str(self.company.vid)+"_"+str(self.sku)

# class ProductConfigurableOfMultiple(models.Model):
#     sku=models.CharField(max_length=globals.SKU_LENGTH)
#     company=models.ForeignKey(Company,on_delete=models.CASCADE)
#     products=models.ManyToManyField(ProductMultiple)
#     variations=models.TextField()
#     int_eav=models.ManyToManyField(ProductIntEav,blank=True)
#     char_eav=models.ManyToManyField(ProductCharEav,blank=True)
#     text_eav=models.ManyToManyField(ProductTextEav,blank=True)
#     decimal_eav=models.ManyToManyField(ProductDecimalEav,blank=True)
#     boolean_eav=models.ManyToManyField(ProductBooleanEav,blank=True)
#     url_eav=models.ManyToManyField(ProductUrlEav,blank=True)
#     class Meta:
#         unique_together = ('sku','company')
    
#     def __str__(self):
#         return str(self.company.vid)+"_"+str(self.sku)

