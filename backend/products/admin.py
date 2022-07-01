from django.contrib import admin
from django.contrib.admin import ModelAdmin
# Register your models here.

from .models import ProductSimple,ProductMultiple,ProductBulk,ProductConfigurable
from .models import ProductBulkOfMultiple,ProductBulkOfBulk
from .models import ProductMultipleOfBulk,ProductMultipleOfMultiple
from .models import ProductConfigurableOfMultiple,ProductConfigurableOfBulk
from .models import ProductBooleanEav,ProductCharEav,ProductIntEav,ProductTextEav,ProductDecimalEav,ProductUrlEav
from .models import Attribute
admin.site.register(ProductSimple)
admin.site.register(ProductMultiple)
admin.site.register(ProductBulk)
admin.site.register(ProductConfigurable)
admin.site.register(ProductMultipleOfBulk)
admin.site.register(ProductMultipleOfMultiple)
admin.site.register(ProductBulkOfBulk)
admin.site.register(ProductBulkOfMultiple)
admin.site.register(ProductConfigurableOfBulk)
admin.site.register(ProductConfigurableOfMultiple)
admin.site.register(ProductIntEav)
admin.site.register(ProductBooleanEav)
admin.site.register(ProductTextEav)
admin.site.register(ProductUrlEav)



class AttributeAdmin(ModelAdmin):
    list_display =  ('name','company','description','type','classification',"variation")
    search_fields = ('name','description','type','classification',"variation")
admin.site.register(Attribute,AttributeAdmin)


class ProductCharEavAdmin(ModelAdmin):
    list_display =  ('sku','company','attribute','value','marketplace')
    search_fields = ('sku','attribute',)
admin.site.register(ProductCharEav,ProductCharEavAdmin)

class ProductDecimalEavAdmin(ModelAdmin):
    list_display =  ('sku','company','attribute','value','marketplace')
    search_fields = ('sku','attribute',)
admin.site.register(ProductDecimalEav,ProductDecimalEavAdmin)

