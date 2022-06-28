from django.contrib import admin
from .models import Shipping,Courier,ShippingList
# Register your models here.
admin.site.register(Courier)
admin.site.register(Shipping)
admin.site.register(ShippingList)