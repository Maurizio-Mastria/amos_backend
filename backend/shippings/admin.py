from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Shipping,Courier,ShippingList
# Register your models here.


class CourierAdmin(ModelAdmin):
    list_display = [field.name for field in Courier._meta.fields]

class ShippingAdmin(ModelAdmin):
    list_display = [field.name for field in Shipping._meta.fields]

class ShippingListAdmin(ModelAdmin):
    list_display = [field.name for field in ShippingList._meta.fields]

admin.site.register(Courier,CourierAdmin)
admin.site.register(Shipping,ShippingAdmin)
admin.site.register(ShippingList,ShippingListAdmin)