from django.db import models
from companies.models import Company
from marketplaces.models import Marketplace
from django.utils import timezone
from backend import globals
from shippings.models import Shipping
from customers.models import Customer
from products.models import ProductBulk,ProductSimple,ProductMultiple
from stocks.models import StockBulkProduct,StockMultipleProduct,StockSimpleProduct

# Create your models here.


class OrderDetail(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH,verbose_name="SKU prodotto")
    qty=models.PositiveIntegerField(verbose_name="Quantità acquistata")
    title=models.CharField(max_length=50,null=True,verbose_name='Titolo prodotto')
    company=models.ForeignKey(Company,on_delete=models.CASCADE,null=True)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE,null=True)
    price=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Prezzo articolo")
    iva=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="IVA articolo")
    shipping_price=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Prezzo spedizione",default=0)
    shipping_iva=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="IVA Spedizione",default=0)
    date=models.DateTimeField(default=timezone.now,verbose_name="Data d'ordine")
    max_shipping_date=models.DateTimeField(blank=True,null=True,verbose_name="Data di spedizione")
    max_consignment_date=models.DateTimeField(blank=True,null=True,verbose_name="Data di consegna")
    payments_date=models.DateTimeField(blank=True,null=True,verbose_name="Data di pagamento")
    business=models.BooleanField(default=False,verbose_name="B2B")
    order_id=models.CharField(max_length=50,verbose_name="ID Ordine del Marketplace",null=True)
    order_item_id=models.CharField(max_length=50,verbose_name="ID Ordine del Prodotto",null=True)
    status=models.CharField(max_length=2,choices=globals.ORDER_STATUS_CHOICES,default="PP",verbose_name="Stato d'ordine")
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True,verbose_name="Cliente")
    shipping=models.ForeignKey(Shipping,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Spedizione")

    def save(self,*args,**kwargs):
        if self.id is None:
            qty=self.qty
        else:
            qty=self.qty-OrderDetail.objects.get(sku=self.sku,company=self.company,marketplace=self.marketplace,order_id=self.order_id,order_item_id=self.order_item_id).qty
        if ProductSimple.objects.filter(company=self.company,sku=self.sku).exists():
            product=ProductSimple.objects.get(company=self.company,sku=self.sku)
            simpleProductStock=StockSimpleProduct.objects.get(company=product.company,product=product)
            simpleProductStock.qty-=qty
            simpleProductStock.save()
        elif ProductBulk.objects.filter(company=self.company,sku=self.sku).exists():
            product=ProductBulk.objects.get(company=self.company,sku=self.sku)
            for product_qty in product.bulk_products_qty.all():
                simpleProductStock=StockSimpleProduct.objects.get(company=product.company,product=product_qty.product)
                simpleProductStock.qty-=(qty*product_qty.qty)
                simpleProductStock.save()
        elif ProductMultiple.objects.filter(company=self.company,sku=self.sku).exists():
            product=ProductMultiple.objects.get(company=self.company,sku=self.sku)
            simpleProductStock=StockSimpleProduct.objects.get(company=product.company,product=product.product)
            simpleProductStock.qty-=(qty*product.qty)
            simpleProductStock.save()
        super(OrderDetail,self).save(*args,*kwargs)



class Order(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    order_detail=models.ManyToManyField(OrderDetail)
    order_id=models.CharField(max_length=50,verbose_name="ID Ordine")
    order_price=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Totale Ordine",null=True)
    order_iva=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Totale IVA",null=True)
    shipping_price=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Totale Spedizione",null=True)
    shipping_iva=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Totale IVA Spedizione",null=True)
    order_total=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Totale Ordine (IVA Incl)",null=True)
    shipping_total=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Totale Spedizione (IVA Incl)",null=True)
    order_shipping_total=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Ordine e Spedizione (IVA Incl)",null=True)
    

    

