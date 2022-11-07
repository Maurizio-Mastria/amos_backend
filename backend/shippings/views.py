from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from backend.mixins import AuthorizationMixin
from .models import Shipping,Courier
from rest_framework import serializers




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



class ShippingViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("shippings")
        return queryset.order_by("id")

class ShippingViewSet(ShippingViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Shipping
    permission_classes = IsAuthenticated
    serializer_class = ShippingSerializer


shipping_list = ShippingViewSet.as_view({'get':'list','post':'create'})
shipping_detail = ShippingViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})


class CourierViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("couriers")
        return queryset.order_by("id")

class CourierViewSet(CourierViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Courier
    permission_class = IsAuthenticated
    serializer_class = CourierSerializer


courier_list = CourierViewSet.as_view({'get':'list','post':'create'})
courier_detail = CourierViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})


# marketplace_router = DefaultRouter()
# marketplace_router.register(r'marketplaces',MarketplaceViewSet)