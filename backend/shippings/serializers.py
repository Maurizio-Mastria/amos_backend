from rest_framework import serializers
from .models import Shipping,Courier




class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'
        read_only_fields =('id','sede','cliente','password','codice')
        depth=0

class ShippingSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Shipping
        fields = '__all__'
        read_only_fields =('id','company','marketplace','create','sent','qty','status','tracking','name','address','city','country')
        depth=0