from rest_framework import serializers
from marketplaces.models import Marketplace
from customers.models import Customer
from shippings.models import Shipping
from companies.models import Company
from .models import Order, OrderDetail


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id',)
        read_only_fields = ('id',)
        depth=0

class MarketplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketplace
        fields = ('id',)
        read_only_fields = ('id',)
        depth=0

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        

class OrderDetailSerializer(serializers.ModelSerializer):
    _status=serializers.CharField(source="get_status_display")
    class Meta:
        model = OrderDetail
        fields = ('id','price','iva','shipping_price','shipping_iva','_status','shipping','customer','sku','qty')
        read_only_fields =('id','price','iva','shipping_price','shipping_iva','_status','shipping','customer','qty')
        depth=1

class OrderSerializer(serializers.ModelSerializer):
    order_detail=OrderDetailSerializer(many=True)
    company=CompanySerializer(read_only=True)
    marketplace=MarketplaceSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ('id','order_id','order_detail','company','marketplace','order_total','order_shipping_total','order_iva','order_price','shipping_price','shipping_iva','shipping_total')
        read_only_fields =('id','order_id',)
        depth=2