from pprint import PrettyPrinter
from django.core.exceptions import ValidationError
from .serializers import CategorySerializer
from xmlrpc.client import boolean
from urllib3 import HTTPResponse
from rest_framework.exceptions import APIException,PermissionDenied
from django.db.utils import IntegrityError
import urllib
from PIL import Image
from io import BytesIO
import base64
import os
from django.conf import settings
from rest_framework.response import Response
import json
from django.core.paginator import Paginator
from companies.models import Company
from marketplaces.models import Marketplace
from backend.mixins import AuthorizationMixin
from django.db.models import Q
from rest_framework import serializers
from .serializers import ProductIntEavSerializer,ProductCharEavSerializer,ProductDecimalEavSerializer,ProductBooleanEavSerializer,ProductTextEavSerializer,ProductUrlEavSerializer
from .models import Category,CustomAttribute,Attribute,DefaultAttribute,ProductSimple,Variation,ProductCharEav,ProductBooleanEav,ProductIntEav,ProductDecimalEav,ProductTextEav,ProductUrlEav
from django.core import serializers
from django.http import JsonResponse
from stocks.models import StockBulkProduct,StockMultipleProduct,StockSimpleProduct
class CustomAttributeViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("products")
        return queryset.order_by("id")

class CategoryViewMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        return queryset.order_by("id")

    def perform_create(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        parent=None
        if serializer.initial_data["parent"] is not None:
            if Category.objects.filter(company=company,marketplace=marketplace,id=serializer.initial_data["parent"]).exists():
                parent=Category.objects.get(company=company,marketplace=marketplace,id=serializer.initial_data["parent"])
        
        try:
            if serializer.is_valid():
                serializer.validated_data["company"]=company
                serializer.validated_data["marketplace"]=marketplace
                serializer.validated_data["parent"]=parent
                serializer.validated_data["attributes"]=serializer.initial_data["attributes"]
                serializer.save()
            else:
                raise APIException(detail="Errore!")
        except IntegrityError:
            raise PermissionDenied(detail="%s errore nella creazione" % (self.model._meta.verbose_name))

    def perform_update(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        parent=None
        if serializer.initial_data["parent"] is not None:
            try:
                parent=Category.objects.get(company=company,marketplace=marketplace,id=serializer.initial_data["parent"])
            except:
                raise PermissionDenied(detail="%s errore nell'aggiornamento" % (self.model._meta.verbose_name))
        try:
            if serializer.is_valid():
                serializer.validated_data["parent"]=parent
                serializer.validated_data["attributes"]=serializer.initial_data["attributes"]
                serializer.save()
            else:
                raise APIException(detail="Errore!")
        except IntegrityError:
            raise PermissionDenied(detail="%s errore nell'aggiornamento" % (self.model._meta.verbose_name))


class CategorySimplifyViewMixin(object):

    def list(self,request):
        
        all_categories={}
        for marketplace in Marketplace.objects.filter(company=self.request.GET.get("company")):
            queryset=super().get_queryset("products").filter(marketplace=marketplace).order_by("id")
            catSerializer=CategorySerializer(queryset,many=True)
            categories=json.loads(json.dumps(catSerializer.data))
            all_categories[marketplace.id]=categories


        def find_parent(tree,id):
            i=0
            while i<len(tree):
                if tree[i]["id"]==id:
                    return tree[i]
                else:
                    if tree[i]["childs"] is not None:
                        obj=find_parent(tree[i]["childs"],id)
                        if obj!=None:
                            return obj
                i+=1
            return None
        trees={}
        for marketid,categories in all_categories.items():
            tree=[]
            i=0
            while len(categories)>0:
                if categories[i]["parent"] is None:
                    tree.append({"id":categories[i]["id"],"childs":[],"title":categories[i]["title"],"name":categories[i]["name"],"attributes":categories[i]["attributes"],"variations":categories[i]["variations"]})
                    categories.pop(i)
                    i=0
                else:
                    parent=find_parent(tree,categories[i]["parent"]["id"])
                    if parent is not None:
                        parent["childs"].append({"id":categories[i]["id"],"childs":[],"title":categories[i]["title"],"name":categories[i]["name"],"attributes":categories[i]["attributes"],"variations":categories[i]["variations"]})
                        categories.pop(i)
                        i=0
                    else:
                        i+=1
            trees[marketid]=tree
        return JsonResponse({"results":trees})

    
    
    

class ProductAttributeViewMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        return queryset.order_by("id")

class ProductSimpleViewMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        return queryset.order_by("id")


    #     return context
        # for attribute in self.request.GET:
        #     if attribute in ["company","marketplace","page","limit"]:
        #         continue

            
                
            
        #     elif attribute == "images":
        #         value=self.request.GET.get("images")
        #         queryset=queryset.filter(url_eav__attribute__icontains="image").exclude(url_eav__value="")
        #         queryset=queryset.order_by('sku').distinct("sku")
        #     elif attribute == "attributes":
        #         values=self.request.GET.get("attributes").split(",")
        #         company=Company.objects.get(id=self.request.GET.get("company"))
        #         for name in values:
                
        #             if Attribute.objects.filter(type="TEXT",name=name,company=company).exists():
        #                 queryset=queryset.filter(text_eav__attribute=name).exclude(text_eav__value="")
        #             elif Attribute.objects.filter(type="URL",name=name,company=company).exists():
        #                 queryset=queryset.filter(url_eav__attribute=name).exclude(url_eav__value="")
        #             elif Attribute.objects.filter(type="DECIMAL",name=name,company=company).exists():
        #                 queryset=queryset.filter(decimal_eav__attribute=name).exclude(decimal_eav__value="")
        #             elif Attribute.objects.filter(type="INT",name=name,company=company).exists():
        #                 queryset=queryset.filter(int_eav__attribute=name).exclude(int_eav__value="")
        #             elif Attribute.objects.filter(type="BOOLEAN",name=name,company=company).exists():
        #                 queryset=queryset.filter(boolean_eav__attribute=name).exclude(boolean_eav__value="")
        #             elif Attribute.objects.filter(type="CHAR",name=name,company=company).exists():
        #                 queryset=queryset.filter(char_eav__attribute=name).exclude(char_eav__value="")
        #             queryset=queryset.order_by('sku').distinct("sku")
        #     else:
        #         value=self.request.GET.get(attribute)[2:]
        #         operator=self.request.GET.get(attribute)[:2]
                

        #         if operator == ">=":
        #             if attribute not in ["sku","gtin","gtin_type"]:
        #                 if queryset.filter(int_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(int_eav__attribute=attribute,int_eav__value__gte=value)
        #                 if queryset.filter(decimal_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(decimal_eav__attribute=attribute,decimal_eav__value__gte=value)

        #         elif operator == "<=":
        #             if attribute not in ["sku","gtin","gtin_type"]:
        #                 if queryset.filter(int_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(int_eav__attribute=attribute,int_eav__value__lte=value)
        #                 if queryset.filter(decimal_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(decimal_eav__attribute=attribute,decimal_eav__value__lte=value)

        #         elif operator == "<>":
        #             if attribute in ["sku","gtin","gtin_type"]:
        #                 queryset=queryset.exclude(**{attribute:value})
        #             else:
        #                 if queryset.filter(char_eav__attribute=attribute).exists():
        #                     queryset=queryset.exclude(char_eav__attribute=attribute,char_eav__value=value)
        #                 if queryset.filter(text_eav__attribute=attribute).exists():
        #                     queryset=queryset.exclude(text_eav__attribute=attribute,text_eav__value=value)
        #                 if queryset.filter(int_eav__attribute=attribute).exists():
        #                     queryset=queryset.exclude(int_eav__attribute=attribute,int_eav__value=value)
        #                 if queryset.filter(decimal_eav__attribute=attribute).exists():
        #                     queryset=queryset.exclude(decimal_eav__attribute=attribute,decimal_eav__value=value)
        #                 if queryset.filter(boolean_eav__attribute=attribute).exists():
        #                     queryset=queryset.exclude(boolean_eav__attribute=attribute,boolean_eav__value=value)
        #                 if queryset.filter(url_eav__attribute=attribute).exists():
        #                     queryset=queryset.exclude(url_eav__attribute=attribute,url_eav__value=value)
        #         elif operator == "==":
        #             if attribute in ["sku","gtin","gtin_type"]:
        #                 queryset=queryset.filter(**{attribute:value})
        #             else:
        #                 if queryset.filter(char_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(char_eav__attribute=attribute,char_eav__value=value)
        #                 if queryset.filter(text_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(text_eav__attribute=attribute,text_eav__value=value)
        #                 if queryset.filter(int_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(int_eav__attribute=attribute,int_eav__value=value)
        #                 if queryset.filter(decimal_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(decimal_eav__attribute=attribute,decimal_eav__value=value)
        #                 if queryset.filter(boolean_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(boolean_eav__attribute=attribute,boolean_eav__value=value)
        #                 if queryset.filter(url_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(url_eav__attribute=attribute,url_eav__value=value)
        #         elif operator == ">>":
        #             if attribute not in ["sku","gtin","gtin_type"]:
        #                 if queryset.filter(int_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(int_eav__attribute=attribute,int_eav__value__gt=value)
        #                 if queryset.filter(decimal_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(decimal_eav__attribute=attribute,decimal_eav__value__gt=value)
        #         elif operator == "<<":
        #             if attribute not in ["sku","gtin","gtin_type"]:
        #                 if queryset.filter(int_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(int_eav__attribute=attribute,int_eav__value__lt=value)
        #                 if queryset.filter(decimal_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(decimal_eav__attribute=attribute,decimal_eav__value__lt=value)
                
        #         elif operator == "cc":
        #             if attribute in ["sku","gtin","gtin_type"]:
        #                 queryset=queryset.filter(**{attribute+'__icontains':value})
        #             else:
        #                 if queryset.filter(char_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(char_eav__attribute=attribute,char_eav__value__icontains=value)
        #                 if queryset.filter(text_eav__attribute=attribute).exists():
        #                     queryset=queryset.filter(text_eav__attribute=attribute,text_eav__value__icontains=value)
        #         elif operator == "nc":
        #             if attribute in ["sku","gtin","gtin_type"]:
        #                 queryset=queryset.exclude(**{attribute+'__icontains':value})
        #             else:
        #                 if queryset.filter(char_eav__attribute=attribute).exists():
        #                     queryset=queryset.exclude(char_eav__attribute=attribute,char_eav__value__icontains=value)
        #                 if queryset.filter(text_eav__attribute=attribute).exists():
        #                     queryset=queryset.exclude(text_eav__attribute=attribute,text_eav__value__icontains=value)
        
        
        
        
        # products=[]
        
        # for obj in page.object_list:
        #     product={}
        #     product["id"]=obj.id
        #     product["sku"]=obj.sku
        #     product["gtin"]=obj.gtin
        #     product["gtin_type"]=obj.gtin_type
        #     product["char_eav"]=[]
        #     product["text_eav"]=[]
        #     product["boolean_eav"]=[]
        #     product["decimal_eav"]=[]
        #     product["url_eav"]=[]
        #     product["int_eav"]=[]
        #     product["char_eav"]=obj.char_eav.filter(marketplace=self.request.GET.get("marketplace")).values()
        #     product["text_eav"]=obj.text_eav.filter(marketplace=self.request.GET.get("marketplace")).values()
        #     product["boolean_eav"]=obj.boolean_eav.filter(marketplace=self.request.GET.get("marketplace")).values()
        #     product["decimal_eav"]=obj.decimal_eav.filter(marketplace=self.request.GET.get("marketplace")).values()
        #     product["int_eav"]=obj.int_eav.filter(marketplace=self.request.GET.get("marketplace")).values()
        #     product["url_eav"]=obj.url_eav.filter(marketplace=self.request.GET.get("marketplace")).values()
        #     products.append(product)
        
        # return Response({"count":pages.count,"next":page.has_next(),"previous":page.has_previous(),"results":products})

    
    # def retrieve(self,request,pk):
    #     queryset=super().get_queryset()
    #     obj=queryset.get(id=pk)
        
    #     product={}
    #     product["id"]=obj.id
    #     product["sku"]=obj.sku
    #     product["gtin"]=obj.gtin
    #     product["gtin_type"]=obj.gtin_type
    #     product["char_eav"]=[]
    #     product["text_eav"]=[]
    #     product["boolean_eav"]=[]
    #     product["decimal_eav"]=[]
    #     product["url_eav"]=[]
    #     product["int_eav"]=[]
    #     product["char_eav"]=obj.char_eav.filter(marketplace=self.request.GET.get("marketplace")).values()
    #     product["text_eav"]=obj.text_eav.filter(marketplace=self.request.GET.get("marketplace")).values()
    #     product["boolean_eav"]=obj.boolean_eav.filter(marketplace=self.request.GET.get("marketplace")).values()
    #     product["decimal_eav"]=obj.decimal_eav.filter(marketplace=self.request.GET.get("marketplace")).values()
    #     product["int_eav"]=obj.int_eav.filter(marketplace=self.request.GET.get("marketplace")).values()
    #     product["url_eav"]=obj.url_eav.filter(marketplace=self.request.GET.get("marketplace")).values()
    #     return Response(product)
        
        

    def perform_create(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        try:
            if serializer.is_valid():
                serializer.validated_data["company"]=company
                serializer.save()
                id=serializer.data["id"]
                stock=StockSimpleProduct(company=company,product=ProductSimple.objects.get(id=id,company=company),qty=0)
                stock.save()
            else:
                raise APIException(detail="Errore!")
        except IntegrityError:
            raise PermissionDenied(detail="%s errore nella creazione" % (self.model._meta.verbose_name))
                
    def perform_update(self,serializer):
        
        # se fa parte di un configurabile non si può cambiare la categoria. La si deve cambiare dal configurabile
        
        company=Company.objects.get(id=self.request.GET.get("company"))
        
        eav_type_objs={}
        for val in ["INT","DECIMAL","BOOLEAN","URL","TEXT","CHAR"]:
            eav_type_objs[val]=[]

        
        for marketplace_id,attributes in serializer.initial_data["marketplace"].items():
            marketplace=Marketplace.objects.get(company=company,id=marketplace_id)
            for attribute,value in attributes.items():
                eav_type=None
                if DefaultAttribute.objects.filter(name=attribute).exists():
                    eav_type=DefaultAttribute.objects.get(name=attribute).type
                elif category.attributes.filter(name=attribute).exists():
                    eav_type=category.attributes.get(name=attribute).type
                elif category.custom_attribute.filter(name=attribute).exists():
                    eav_type=category.custom_attribute.get(name=attribute).type
                else:
                    raise APIException(detail="L'attributo '"+str(attribute)+"' non esiste!")
                
                if eav_type is not None:
                    obj=None
                    if eav_type=="DECIMAL":
                        try:
                            obj=ProductDecimalEav.objects.get(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute)
                            obj.value=value
                        except ProductDecimalEav.DoesNotExist:
                            obj=ProductDecimalEav(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute,value=value)
                        data=json.loads(serializers.serialize("json",[obj,]))
                        fields=data[0]["fields"]
                        fields["id"]=data[0]["pk"]
                        modelSerializer=ProductDecimalEavSerializer(data=fields)
                    elif eav_type=="INT":
                        try:
                            obj=ProductIntEav.objects.get(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute)
                            obj.value=value
                        except ProductIntEav.DoesNotExist:
                            obj=ProductIntEav(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute,value=value)
                        data=json.loads(serializers.serialize("json",[obj,]))
                        fields=data[0]["fields"]
                        fields["id"]=data[0]["pk"]
                        modelSerializer=ProductIntEavSerializer(data=fields)
                    elif eav_type=="URL":
                        try:
                            obj=ProductUrlEav.objects.get(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute)
                            obj.value=value
                        except ProductUrlEav.DoesNotExist:
                            obj=ProductUrlEav(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute,value=value)
                        data=json.loads(serializers.serialize("json",[obj,]))
                        fields=data[0]["fields"]
                        fields["id"]=data[0]["pk"]
                        modelSerializer=ProductUrlEavSerializer(data=fields)
                    elif eav_type=="BOOLEAN":
                        try:
                            obj=ProductBooleanEav.objects.get(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute)
                            obj.value=value
                        except ProductBooleanEav.DoesNotExist:
                            obj=ProductBooleanEav(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute,value=value)
                        data=json.loads(serializers.serialize("json",[obj,]))
                        fields=data[0]["fields"]
                        fields["id"]=data[0]["pk"]
                        modelSerializer=ProductBooleanEavSerializer(data=fields)
                    elif eav_type=="TEXT":
                        try:
                            obj=ProductTextEav.objects.get(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute)
                            obj.value=value
                        except ProductTextEav.DoesNotExist:
                            obj=ProductTextEav(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute,value=value)
                        data=json.loads(serializers.serialize("json",[obj,]))
                        fields=data[0]["fields"]
                        fields["id"]=data[0]["pk"]
                        modelSerializer=ProductTextEavSerializer(data=fields)
                    elif eav_type=="CHAR":
                        try:
                            obj=ProductCharEav.objects.get(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute)
                            obj.value=value
                        except ProductCharEav.DoesNotExist:
                            obj=ProductCharEav(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute,value=value)
                        data=json.loads(serializers.serialize("json",[obj,]))
                        fields=data[0]["fields"]
                        fields["id"]=data[0]["pk"]
                        modelSerializer=ProductCharEavSerializer(data=fields)
                        
                    try:
                        if modelSerializer.is_valid():
                            eav_type_objs[eav_type].append(obj)
                    except ValidationError as e:
                        raise APIException(detail="Il valore dell'attributo '"+str(attribute)+"' non è valido! '''"+str(e)+"'''")
            

        try:
            if serializer.is_valid():
                serializer.save()
                productObj=ProductSimple.objects.get(id=serializer.data["id"])
                productObj.category=category
                productObj.save()
                for eav_type,eav_objs in eav_type_objs.items():
                    for eav_obj in eav_objs:
                        eav_obj.save()
                        if eav_type=="INT" and eav_obj not in productObj.int_eav.all():
                            productObj.int_eav.add(eav_obj)
                        elif eav_type=="DECIMAL" and eav_obj not in productObj.decimal_eav.all():
                            productObj.decimal_eav.add(eav_obj)
                        elif eav_type=="URL" and eav_obj not in productObj.url_eav.all():
                            productObj.url_eav.add(eav_obj)
                        elif eav_type=="BOOLEAN" and eav_obj not in productObj.boolean_eav.all():
                            productObj.boolean_eav.add(eav_obj)
                        elif eav_type=="TEXT" and eav_obj not in productObj.text_eav.all():
                            productObj.text_eav.add(eav_obj)
                        elif eav_type=="CHAR" and eav_obj not in productObj.char_eav.all():
                            productObj.char_eav.add(eav_obj)
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