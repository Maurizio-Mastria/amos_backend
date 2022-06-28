from rest_framework import serializers
from .models import Inventory,InventoryDimension,InventoryOffer,IVA



class IVASerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IVA
        fields = ('id','code','percentage')
        read_only_fields =('id','code','percentage')

class InventoryOfferSerializer(serializers.ModelSerializer):
    iva=IVASerializer()
    buy_iva=IVASerializer()
    class Meta:
        model = InventoryOffer
        fields = ('id','marketplace','price','is_min_max','min_price','max_price','buy_price','buy_iva','offer_price','start_offer','end_offer','iva','is_active')
        read_only_fields =('id','marketplace',)


class InventoryDimensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryDimension
        fields = ('id','weight','volume','length','height','width')
        read_only_fields =('id',)

class InventorySerializer(serializers.ModelSerializer):
    offer=InventoryOfferSerializer(many=True)
    dimension=InventoryDimensionSerializer()
    class Meta:
        model = Inventory
        fields = ('id','sku','company','offer','dimension')
        read_only_fields =('id','company')
