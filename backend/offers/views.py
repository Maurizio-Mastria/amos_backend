from django.shortcuts import render
from rest_framework import serializers

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from backend.mixins import AuthorizationMixin
from .models import ProductSimpleOffer,ProductBulkOffer,ProductMultipleOffer
from marketplaces.models import Marketplace
# Create your views here.

class ProductSimpleOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSimpleOffer
        fields = '__all__'

    def validate(self, data):
        if data["marketplace"].company!=data["company"]:
            raise serializers.ValidationError("Company/marketplace errati")
        return data

class ProductMultipleOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMultipleOffer
        fields = '__all__'

    def validate(self, data):
        if data["marketplace"].company!=data["company"]:
            raise serializers.ValidationError("Company/marketplace errati")
        return data

class ProductBulkOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBulkOffer
        fields = '__all__'

    def validate(self, data):
        if data["marketplace"].company!=data["company"]:
            raise serializers.ValidationError("Company/marketplace errati")
        return data
        
class ProductSimpleOfferViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("offers")
        return queryset.order_by("id")

class ProductMultipleOfferViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("offers")
        return queryset.order_by("id")

class ProductBulkOfferViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("offers")
        return queryset.order_by("id")

    


class ProductSimpleOfferViewSet(ProductSimpleOfferViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductSimpleOffer
    permission_class = IsAuthenticated
    serializer_class = ProductSimpleOfferSerializer

product_simple_offers_list = ProductSimpleOfferViewSet.as_view({'get':'list','post':'create'})
product_simple_offer_detail = ProductSimpleOfferViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})


class ProductMultipleOfferViewSet(ProductMultipleOfferViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductMultipleOffer
    permission_class = IsAuthenticated
    serializer_class = ProductMultipleOfferSerializer

product_multiple_offers_list = ProductMultipleOfferViewSet.as_view({'get':'list','post':'create'})
product_multiple_offer_detail = ProductMultipleOfferViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

class ProductBulkOfferViewSet(ProductBulkOfferViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductBulkOffer
    permission_class = IsAuthenticated
    serializer_class = ProductBulkOfferSerializer

product_bulk_offers_list = ProductBulkOfferViewSet.as_view({'get':'list','post':'create'})
product_bulk_offer_detail = ProductBulkOfferViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})
