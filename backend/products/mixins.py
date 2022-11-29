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
from .models import Category,CustomAttribute,Attribute,DefaultAttribute
from .models import ProductSimple,ProductConfigurable,ProductMultiple,ProductBulk
from .models import ProductCharEav,ProductBooleanEav,ProductIntEav,ProductDecimalEav,ProductTextEav,ProductUrlEav
from django.core import serializers
from django.http import JsonResponse
from stocks.models import StockBulkProduct,StockMultipleProduct,StockSimpleProduct
from django.core.exceptions import ObjectDoesNotExist

class CustomAttributeViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("products")
        return queryset.order_by("id")

    def perform_create(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        if serializer.is_valid():
            serializer.validated_data["company"]=company
            serializer.save()

class CategoryViewMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        queryset=queryset.filter(marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace")))
        if self.request.GET.get("simple"):
            queryset=queryset.filter(simple__id=self.request.GET.get("simple"))
        if self.request.GET.get("configurable"):
            queryset=queryset.filter(configurable__id=self.request.GET.get("configurable"))
        if self.request.GET.get("bulk"):
            queryset=queryset.filter(bulk__id=self.request.GET.get("bulk"))
        if self.request.GET.get("multiple"):
            queryset=queryset.filter(multiple__id=self.request.GET.get("multiple"))
        return queryset.order_by("id")

    def perform_create(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        otherMarketplaces=Marketplace.objects.filter(account=marketplace.account,code=marketplace.code,company=marketplace.company).exclude(id=marketplace.id)
        otherParents=None
        parent=None
        if serializer.initial_data["parent"] is not None:
            if Category.objects.filter(company=company,marketplace=marketplace,id=serializer.initial_data["parent"]).exists():
                parent=Category.objects.get(company=company,marketplace=marketplace,id=serializer.initial_data["parent"])
                otherParents=Category.objects.filter(company=parent.company,marketplace__code=parent.marketplace.code,marketplace__account=parent.marketplace.account).exclude(id=parent.id)
            
        try:
            if serializer.is_valid():
                serializer.validated_data["company"]=company
                serializer.validated_data["marketplace"]=marketplace
                serializer.validated_data["parent"]=parent
                serializer.save()
                for market in otherMarketplaces:
                    data={}
                    data["title"]=serializer.initial_data["title"]
                    data["name"]=serializer.initial_data["name"]
                    newSerializer=CategorySerializer(data=data)
                    if newSerializer.is_valid():
                        newSerializer.validated_data["company"]=company
                        newSerializer.validated_data["marketplace"]=market
                        if otherParents is not None:
                            newSerializer.validated_data["parent"]=Category.objects.get(id=otherParents.get(marketplace=market).id,company=company)
                        else:
                            newSerializer.validated_data["parent"]=None
                        newSerializer.save()
            else:
                raise APIException(detail="Errore!")
        except IntegrityError:
            raise PermissionDenied(detail="%s errore nella creazione" % (self.model._meta.verbose_name))

    def perform_update(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        otherMarketplaces=Marketplace.objects.filter(account=marketplace.account,code=marketplace.code,company=marketplace.company).exclude(id=marketplace.id)
        otherParents=None
        newData={}
        
        for market in otherMarketplaces:
            newData[market]={}
        
        if "parent" in serializer.initial_data:
            if serializer.initial_data["parent"] is not None:
                try:
                    parent=Category.objects.get(company=company,marketplace=marketplace,id=serializer.initial_data["parent"])
                    serializer.validated_data["parent"]=parent
                    otherParents=Category.objects.filter(company=parent.company,marketplace__code=parent.marketplace.code,marketplace__account=parent.marketplace.account,name=parent.name).exclude(id=parent.id)
                    for oParent in otherParents:
                        newData[oParent.marketplace]["parent"]=oParent
                except:
                    raise PermissionDenied(detail="%s errore nell'aggiornamento" % (self.model._meta.verbose_name))
            else:
                serializer.validated_data["parent"]=None
                for market in otherMarketplaces:
                    newData[market]["parent"]=None
        if "attributes" in serializer.initial_data:
            serializer.validated_data["attributes"]=serializer.initial_data["attributes"]
            for market in otherMarketplaces:
                newData[market]["attributes"]=serializer.initial_data["attributes"]
        if "custom_attributes" in serializer.initial_data:
            serializer.validated_data["custom_attributes"]=serializer.initial_data["custom_attributes"]
            for market in otherMarketplaces:
                newData[market]["custom_attributes"]=serializer.initial_data["custom_attributes"]

        if "variations" in serializer.initial_data:
            serializer.validated_data["variations"]=serializer.initial_data["variations"]
            for market in otherMarketplaces:
                newData[market]["variations"]=serializer.initial_data["variations"]

        if "custom_variations" in serializer.initial_data:
            serializer.validated_data["custom_variations"]=serializer.initial_data["custom_variations"]
            for market in otherMarketplaces:
                newData[market]["custom_variations"]=serializer.initial_data["custom_variations"]

        if "_simple" in serializer.initial_data:
            if len(serializer.initial_data["_simple"]) is not None:
                try:
                    simple=ProductSimple.objects.filter(company=company,id__in=serializer.initial_data["_simple"])
                    serializer.validated_data["simple"]=simple
                    for market in otherMarketplaces:
                        newData[market]["simple"]=simple
                except:
                    raise PermissionDenied(detail="%s errore nell'aggiornamento" % (self.model._meta.verbose_name))
            else:
                serializer.validated_data["simple"]=None
                for market in otherMarketplaces:
                    newData[market]["simple"]=None

        if "_configurable" in serializer.initial_data:
            if len(serializer.initial_data["_configurable"]) is not None:
                try:
                    configurable=ProductConfigurable.objects.filter(company=company,id__in=serializer.initial_data["_configurable"])
                    serializer.validated_data["configurable"]=configurable
                    for market in otherMarketplaces:
                        newData[market]["configurable"]=configurable
                except:
                    raise PermissionDenied(detail="%s errore nell'aggiornamento" % (self.model._meta.verbose_name))
            else:
                serializer.validated_data["configurable"]=None
                for market in otherMarketplaces:
                    newData[market]["configurable"]=None

        if "_bulk" in serializer.initial_data:
            if len(serializer.initial_data["_bulk"]) is not None:
                try:
                    bulk=ProductBulk.objects.filter(company=company,id__in=serializer.initial_data["_bulk"])
                    serializer.validated_data["bulk"]=bulk
                    for market in otherMarketplaces:
                        newData[market]["bulk"]=bulk
                except:
                    raise PermissionDenied(detail="%s errore nell'aggiornamento" % (self.model._meta.verbose_name))
            else:
                serializer.validated_data["bulk"]=None
                for market in otherMarketplaces:
                    newData[market]["bulk"]=None
        if "_multiple" in serializer.initial_data:
            if len(serializer.initial_data["_multiple"]) is not None:
                try:
                    multiple=ProductMultiple.objects.filter(company=company,id__in=serializer.initial_data["_multiple"])
                    serializer.validated_data["multiple"]=multiple
                    for market in otherMarketplaces:
                        newData[market]["multiple"]=multiple
                except:
                    raise PermissionDenied(detail="%s errore nell'aggiornamento" % (self.model._meta.verbose_name))
            else:
                serializer.validated_data["multiple"]=None
                for market in otherMarketplaces:
                    newData[market]["multiple"]=None
        
        try:
            if serializer.is_valid():
                thisCategory=Category.objects.get(company=company,marketplace=marketplace,id=serializer.instance.id)
                saved=serializer.save()
                otherCategories=Category.objects.filter(company=company,marketplace__in=otherMarketplaces,name=thisCategory.name).exclude(id=thisCategory.id)
                for market,data in newData.items():
                    print(data)
                    category=otherCategories.get(company=company,marketplace=market)
                    if "title" not in data:
                        data["title"]=saved.title
                    if "name" not in data:
                        data["name"]=saved.name
                    newSerializer=CategorySerializer(instance=category,data=data)
                    if newSerializer.is_valid():
                        for key,value in data.items():
                            newSerializer.validated_data[key]=value
                        newSerializer.save()
                    else:
                        raise APIException(detail=newSerializer.errors)
            else:
                raise APIException(detail="Errore!")
        except IntegrityError:
            raise PermissionDenied(detail="%s errore nell'aggiornamento" % (self.model._meta.verbose_name))


class CategorySimplifyViewMixin(object):

    def list(self,request):
        all_categories={}
        marketplace=Marketplace.objects.get(company=self.request.GET.get("company"),id=self.request.GET.get("marketplace"))
        queryset=super().get_queryset("products").filter(marketplace=marketplace).order_by("id")
        catSerializer=CategorySerializer(queryset,many=True)
        categories=json.loads(json.dumps(catSerializer.data))

        def find_parent(atree,id):
            i=0
            while i<len(atree):
                if atree[i]["id"]==id:
                    return atree[i]
                else:
                    if atree[i]["childs"] is not None:
                        obj=find_parent(atree[i]["childs"],id)
                        if obj!=None:
                            return obj
                i+=1
            return None
        
        tree=[]
        
        i=0
        while len(categories)>0:
            if categories[i]["parent"] is None:
                tree.append(
                    {
                        "id":categories[i]["id"],
                        "childs":[],
                        "title":categories[i]["title"],
                        "name":categories[i]["name"],
                        "attributes":categories[i]["attributes"],
                        "custom_attributes":categories[i]["custom_attributes"],
                        "variations":categories[i]["variations"],
                        "custom_variations":categories[i]["custom_variations"],
                        'simple':categories[i]["simple"],
                        'bulk':categories[i]["bulk"],
                        'configurable':categories[i]["configurable"],
                        'multiple':categories[i]["multiple"],
                        'parent':categories[i]["parent"]
                        })
                categories.pop(i)
                i=0
            else:
                parent=find_parent(tree,categories[i]["parent"]["id"])
                if parent is not None:
                    parent["childs"].append(
                    {
                        "id":categories[i]["id"],
                        "childs":[],
                        "title":categories[i]["title"],
                        "name":categories[i]["name"],
                        "attributes":categories[i]["attributes"],
                        "custom_attributes":categories[i]["custom_attributes"],
                        "variations":categories[i]["variations"],
                        "custom_variations":categories[i]["custom_variations"],
                        'simple':categories[i]["simple"],
                        'bulk':categories[i]["bulk"],
                        'configurable':categories[i]["configurable"],
                        'multiple':categories[i]["multiple"],
                        'parent':categories[i]["parent"]
                        })
                    categories.pop(i)
                    i=0
                else:
                    i+=1
        
        return JsonResponse({"results":tree})

    
    
    

class ProductAttributeViewMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        return queryset.order_by("id")

class ProductSimpleViewMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        search=None
        if self.request.GET.get("search"):
            search=self.request.GET.get("search")
            marketplace=self.request.GET.get("marketplace")
            queryset=queryset.filter(sku__icontains=search)|queryset.filter(gtin__contains=search)\
                |queryset.filter(char_eav__value__icontains=search,char_eav__marketplace=marketplace)\
                |queryset.filter(text_eav__value__icontains=search,text_eav__marketplace=marketplace)
            return queryset.order_by("id").distinct()
                

        return queryset.order_by("id")


        
        

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
        
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        simple=ProductSimple.objects.get(company=company,sku=serializer.validated_data["sku"])
        
        eav_type_objs={}
        for val in ["INT","DECIMAL","BOOLEAN","URL","TEXT","CHAR"]:
            eav_type_objs[val]=[]
        
        
        for attribute,value in serializer.initial_data["marketplace"][str(marketplace.id)].items():
            eav_type=None
            
            if DefaultAttribute.objects.filter(name=attribute).exists():
                eav_type=DefaultAttribute.objects.get(name=attribute).type
            elif Attribute.objects.filter(name=attribute).exists():
                eav_type=Attribute.objects.get(name=attribute).type
            elif marketplace.code=="AMZ" and attribute=="asin":
                eav_type="CHAR"
            
            else:
                raise APIException(detail="L'attributo '"+str(attribute)+"' non esiste!")
            
            if eav_type is not None:
                obj=None
                if eav_type=="DECIMAL":
                    if "value" in value and "unit" in value:
                        try:
                            obj=ProductDecimalEav.objects.get(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute)
                            obj.value=value["value"]
                            obj.unit=value["unit"]
                            print(obj.unit)
                        except ProductDecimalEav.DoesNotExist:
                            obj=ProductDecimalEav(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute,value=value["value"],unit=value["unit"])
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

                if eav_type=="DECIMAL" and "value" in value and value["value"] in ["",None] and obj.id:
                    obj.delete()
                elif eav_type=="DECIMAL" and ("value" not in value or "unit" not in value):
                    pass
                elif  eav_type!="DECIMAL" and value in ["",None] and obj.id:
                    obj.delete()
                else:
                    try:
                        if modelSerializer.is_valid():
                            eav_type_objs[eav_type].append(obj)
                    except ValidationError as e:
                        raise APIException(detail="Il valore dell'attributo '"+str(attribute)+"' non è valido! '''"+str(e)+"'''")
            

        try:
            if serializer.is_valid():
                serializer.save()
                productObj=ProductSimple.objects.get(id=serializer.data["id"])
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


class ProductConfigurableViewMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        search=None
        if self.request.GET.get("search"):
            search=self.request.GET.get("search")
            marketplace=self.request.GET.get("marketplace")
            queryset=queryset.filter(sku__icontains=search)|queryset.filter(gtin__contains=search)\
                |queryset.filter(char_eav__value__icontains=search,char_eav__marketplace=marketplace)\
                |queryset.filter(text_eav__value__icontains=search,text_eav__marketplace=marketplace)
            return queryset.order_by("id").distinct()
                

        return queryset.order_by("id")

class ProductBulkViewMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        search=None
        if self.request.GET.get("search"):
            search=self.request.GET.get("search")
            marketplace=self.request.GET.get("marketplace")
            queryset=queryset.filter(sku__icontains=search)|queryset.filter(gtin__contains=search)\
                |queryset.filter(char_eav__value__icontains=search,char_eav__marketplace=marketplace)\
                |queryset.filter(text_eav__value__icontains=search,text_eav__marketplace=marketplace)
            return queryset.order_by("id").distinct()
                

        return queryset.order_by("id")

class ProductMultipleViewMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        search=None
        if self.request.GET.get("search"):
            search=self.request.GET.get("search")
            marketplace=self.request.GET.get("marketplace")
            queryset=queryset.filter(sku__icontains=search)|queryset.filter(gtin__contains=search)\
                |queryset.filter(char_eav__value__icontains=search,char_eav__marketplace=marketplace)\
                |queryset.filter(text_eav__value__icontains=search,text_eav__marketplace=marketplace)
            return queryset.order_by("id").distinct()
                

        return queryset.order_by("id")