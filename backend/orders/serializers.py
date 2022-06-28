from rest_framework import serializers
from .models import Order, OrderDetail




class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'
        read_only_fields =('id','price','iva','shipping_price','shipping_iva')

class OrderSerializer(serializers.ModelSerializer):
    detail=OrderDetailSerializer
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields =('id','company','marketplace','order_id','date','detail','status')