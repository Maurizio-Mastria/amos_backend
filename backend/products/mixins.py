from urllib3 import HTTPResponse
from rest_framework.exceptions import APIException,PermissionDenied
from companies.models import Company
from django.db.utils import IntegrityError
from products.models import Attribute
import urllib
from PIL import Image
from io import BytesIO
import base64
import os
from django.conf import settings
from rest_framework.response import Response
class ProductMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset()
        
        for attribute in self.request.GET:
            if attribute=="company":
                continue

            if attribute == "marketplace":
                value=self.request.GET.get("marketplace")
                queryset=queryset.filter(char_eav__marketplace=value)|\
                    queryset.filter(text_eav__marketplace=value)|\
                        queryset.filter(int_eav__marketplace=value)|\
                            queryset.filter(decimal_eav__marketplace=value)|\
                                queryset.filter(boolean_eav__marketplace=value)|\
                                    queryset.filter(url_eav__marketplace=value)
                queryset=queryset.order_by('sku').distinct("sku")
                
            
            elif attribute == "images":
                value=self.request.GET.get("images")
                queryset=queryset.filter(url_eav__attribute__icontains="image").exclude(url_eav__value="")
                queryset=queryset.order_by('sku').distinct("sku")
            elif attribute == "attributes":
                values=self.request.GET.get("attributes").split(",")
                company=Company.objects.get(id=self.request.GET.get("company"))
                for name in values:
                
                    if Attribute.objects.filter(type="TEXT",name=name,company=company).exists():
                        queryset=queryset.filter(text_eav__attribute=name).exclude(text_eav__value="")
                    elif Attribute.objects.filter(type="URL",name=name,company=company).exists():
                        queryset=queryset.filter(url_eav__attribute=name).exclude(url_eav__value="")
                    elif Attribute.objects.filter(type="DECIMAL",name=name,company=company).exists():
                        queryset=queryset.filter(decimal_eav__attribute=name).exclude(decimal_eav__value="")
                    elif Attribute.objects.filter(type="INT",name=name,company=company).exists():
                        queryset=queryset.filter(int_eav__attribute=name).exclude(int_eav__value="")
                    elif Attribute.objects.filter(type="BOOLEAN",name=name,company=company).exists():
                        queryset=queryset.filter(boolean_eav__attribute=name).exclude(boolean_eav__value="")
                    elif Attribute.objects.filter(type="CHAR",name=name,company=company).exists():
                        queryset=queryset.filter(char_eav__attribute=name).exclude(char_eav__value="")
                    queryset=queryset.order_by('sku').distinct("sku")
            else:
                value=self.request.GET.get(attribute)[2:]
                operator=self.request.GET.get(attribute)[:2]
                

                if operator == ">=":
                    if attribute not in ["sku","gtin","gtin_type"]:
                        if queryset.filter(int_eav__attribute=attribute).exists():
                            queryset=queryset.filter(int_eav__attribute=attribute,int_eav__value__gte=value)
                        if queryset.filter(decimal_eav__attribute=attribute).exists():
                            queryset=queryset.filter(decimal_eav__attribute=attribute,decimal_eav__value__gte=value)

                elif operator == "<=":
                    if attribute not in ["sku","gtin","gtin_type"]:
                        if queryset.filter(int_eav__attribute=attribute).exists():
                            queryset=queryset.filter(int_eav__attribute=attribute,int_eav__value__lte=value)
                        if queryset.filter(decimal_eav__attribute=attribute).exists():
                            queryset=queryset.filter(decimal_eav__attribute=attribute,decimal_eav__value__lte=value)

                elif operator == "<>":
                    if attribute in ["sku","gtin","gtin_type"]:
                        queryset=queryset.exclude(**{attribute:value})
                    else:
                        if queryset.filter(char_eav__attribute=attribute).exists():
                            queryset=queryset.exclude(char_eav__attribute=attribute,char_eav__value=value)
                        if queryset.filter(text_eav__attribute=attribute).exists():
                            queryset=queryset.exclude(text_eav__attribute=attribute,text_eav__value=value)
                        if queryset.filter(int_eav__attribute=attribute).exists():
                            queryset=queryset.exclude(int_eav__attribute=attribute,int_eav__value=value)
                        if queryset.filter(decimal_eav__attribute=attribute).exists():
                            queryset=queryset.exclude(decimal_eav__attribute=attribute,decimal_eav__value=value)
                        if queryset.filter(boolean_eav__attribute=attribute).exists():
                            queryset=queryset.exclude(boolean_eav__attribute=attribute,boolean_eav__value=value)
                        if queryset.filter(url_eav__attribute=attribute).exists():
                            queryset=queryset.exclude(url_eav__attribute=attribute,url_eav__value=value)
                elif operator == "==":
                    if attribute in ["sku","gtin","gtin_type"]:
                        queryset=queryset.filter(**{attribute:value})
                    else:
                        if queryset.filter(char_eav__attribute=attribute).exists():
                            queryset=queryset.filter(char_eav__attribute=attribute,char_eav__value=value)
                        if queryset.filter(text_eav__attribute=attribute).exists():
                            queryset=queryset.filter(text_eav__attribute=attribute,text_eav__value=value)
                        if queryset.filter(int_eav__attribute=attribute).exists():
                            queryset=queryset.filter(int_eav__attribute=attribute,int_eav__value=value)
                        if queryset.filter(decimal_eav__attribute=attribute).exists():
                            queryset=queryset.filter(decimal_eav__attribute=attribute,decimal_eav__value=value)
                        if queryset.filter(boolean_eav__attribute=attribute).exists():
                            queryset=queryset.filter(boolean_eav__attribute=attribute,boolean_eav__value=value)
                        if queryset.filter(url_eav__attribute=attribute).exists():
                            queryset=queryset.filter(url_eav__attribute=attribute,url_eav__value=value)
                elif operator == ">>":
                    if attribute not in ["sku","gtin","gtin_type"]:
                        if queryset.filter(int_eav__attribute=attribute).exists():
                            queryset=queryset.filter(int_eav__attribute=attribute,int_eav__value__gt=value)
                        if queryset.filter(decimal_eav__attribute=attribute).exists():
                            queryset=queryset.filter(decimal_eav__attribute=attribute,decimal_eav__value__gt=value)
                elif operator == "<<":
                    if attribute not in ["sku","gtin","gtin_type"]:
                        if queryset.filter(int_eav__attribute=attribute).exists():
                            queryset=queryset.filter(int_eav__attribute=attribute,int_eav__value__lt=value)
                        if queryset.filter(decimal_eav__attribute=attribute).exists():
                            queryset=queryset.filter(decimal_eav__attribute=attribute,decimal_eav__value__lt=value)
                
                elif operator == "cc":
                    if attribute in ["sku","gtin","gtin_type"]:
                        queryset=queryset.filter(**{attribute+'__icontains':value})
                    else:
                        if queryset.filter(char_eav__attribute=attribute).exists():
                            queryset=queryset.filter(char_eav__attribute=attribute,char_eav__value__icontains=value)
                        if queryset.filter(text_eav__attribute=attribute).exists():
                            queryset=queryset.filter(text_eav__attribute=attribute,text_eav__value__icontains=value)
                elif operator == "nc":
                    if attribute in ["sku","gtin","gtin_type"]:
                        queryset=queryset.exclude(**{attribute+'__icontains':value})
                    else:
                        if queryset.filter(char_eav__attribute=attribute).exists():
                            queryset=queryset.exclude(char_eav__attribute=attribute,char_eav__value__icontains=value)
                        if queryset.filter(text_eav__attribute=attribute).exists():
                            queryset=queryset.exclude(text_eav__attribute=attribute,text_eav__value__icontains=value)
        
        return queryset.order_by('sku').distinct("sku")

    def perform_create(self,serializer):
        print(serializer.validated_data)
        try:
            if serializer.is_valid():
                serializer.save()
            else:
                raise APIException(detail="Errore!")
        except IntegrityError:
            raise PermissionDenied(detail="%s già esistente" % (self.model._meta.verbose_name))
                
    def perform_update(self,serializer):
        try:
            if serializer.is_valid():
                serializer.save()
            else:
                raise APIException(detail="Errore!")
        except IntegrityError:
            raise PermissionDenied(detail="%s già esistente" % (self.model._meta.verbose_name))

    



class AbstractProductListMixin(object):
    def get_queryset(self):
        
        
        marketplace=self.request.GET.get("marketplace")
        queryset=queryset.filter(char_eav__marketplace=marketplace)|\
            queryset.filter(text_eav__marketplace=marketplace)|\
                queryset.filter(int_eav__marketplace=marketplace)|\
                    queryset.filter(decimal_eav__marketplace=marketplace)|\
                        queryset.filter(boolean_eav__marketplace=marketplace)|\
                            queryset.filter(url_eav__marketplace=marketplace)
        queryset=queryset.order_by('sku').distinct("sku")