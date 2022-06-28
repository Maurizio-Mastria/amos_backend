from rest_framework import serializers
from .models import Marketplace

class MarketplaceSerializer(serializers.ModelSerializer):
    _code=serializers.CharField(source="get_code_display")
    _country=serializers.CharField(source="get_country_display")

    class Meta:
        model = Marketplace
        fields = ('id','country','code','status','website','company','_code','_country')
        read_only_fields =('id','name','_code','_country')