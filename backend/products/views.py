from pprint import PrettyPrinter
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_condition import Or,And
from backend.permissions import IsSuperUser,IsVendor,IsStaff,IsVendorStaff,IsVendorCollaborator
from .serializers import ProductSimpleSerializer,ProductMultipleSerializer,ProductConfigurableSerializer,ProductBulkSerializer
from .serializers import ProductBulkOfBulkSerializer,ProductBulkOfMultipleSerializer,ProductMultipleOfBulkSerializer,ProductMultipleOfMultipleSerializer
from .serializers import ProductConfigurableOfBulkSerializer,ProductConfigurableOfMultipleSerializer
from .serializers import ProductIntEavSerializer,ProductCharEavSerializer,ProductDecimalEavSerializer,ProductBooleanEavSerializer,ProductTextEavSerializer,ProductUrlEavSerializer
from .serializers import AttributeSerializer
from products.mixins import ProductMixin
from backend.mixins import CompanyModelMixin,GenericModelMixin
from .models import ProductSimple,ProductMultiple,ProductBulk,ProductConfigurable
from .models import ProductBulkOfMultiple,ProductBulkOfBulk
from .models import ProductMultipleOfBulk,ProductMultipleOfMultiple
from .models import ProductConfigurableOfMultiple,ProductConfigurableOfBulk
from .models import ProductBooleanEav,ProductCharEav,ProductIntEav,ProductTextEav,ProductDecimalEav,ProductUrlEav
from .models import Attribute
from django.views import View
from companies.models import Company
from marketplaces.models import Marketplace
from rest_framework.exceptions import APIException,PermissionDenied
from PIL import Image
import shutil
import re
import base64
from io import BytesIO
import os
from django.conf import settings
# Create your views here.
class ProductSimpleViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductSimple
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductSimpleSerializer

product_simple_list = ProductSimpleViewSet.as_view({'get':'list'})
product_simple_detail = ProductSimpleViewSet.as_view({'get':'retrieve'})

class ProductMultipleViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductMultiple
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductMultipleSerializer

product_multiple_list = ProductMultipleViewSet.as_view({'get':'list'})
product_multiple_detail = ProductMultipleViewSet.as_view({'get':'retrieve','delete':'destroy'})

class ProductBulkViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductBulk
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductBulkSerializer

product_bulk_list = ProductBulkViewSet.as_view({'get':'list'})
product_bulk_detail = ProductBulkViewSet.as_view({'get':'retrieve','delete':'destroy'})

class ProductConfigurableViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductConfigurable
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductConfigurableSerializer

product_configurable_list = ProductConfigurableViewSet.as_view({'get':'list'})
product_configurable_detail = ProductConfigurableViewSet.as_view({'get':'retrieve','delete':'destroy'})

class ProductBulkOfBulkViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductBulkOfBulk
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductBulkOfBulkSerializer

product_bulk_of_bulk_list = ProductBulkOfBulkViewSet.as_view({'get':'list'})
product_bulk_of_bulk_detail = ProductBulkOfBulkViewSet.as_view({'get':'retrieve','delete':'destroy'})

class ProductBulkOfMultipleViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductBulkOfMultiple
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductBulkOfMultipleSerializer

product_bulk_of_multiple_list = ProductBulkOfMultipleViewSet.as_view({'get':'list'})
product_bulk_of_multiple_detail = ProductBulkOfMultipleViewSet.as_view({'get':'retrieve','delete':'destroy'})

class ProductMultipleOfBulkViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductMultipleOfBulk
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductMultipleOfBulkSerializer

product_multiple_of_bulk_list = ProductMultipleOfBulkViewSet.as_view({'get':'list'})
product_multiple_of_bulk_detail = ProductMultipleOfBulkViewSet.as_view({'get':'retrieve','delete':'destroy'})

class ProductMultipleOfMultipleViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductMultipleOfMultiple
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductMultipleOfMultipleSerializer

product_multiple_of_multiple_list = ProductMultipleOfMultipleViewSet.as_view({'get':'list'})
product_multiple_of_multiple_detail = ProductMultipleOfMultipleViewSet.as_view({'get':'retrieve','delete':'destroy'})

class ProductConfigurableOfBulkViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductConfigurableOfBulk
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductConfigurableOfBulkSerializer

product_configurable_of_bulk_list = ProductConfigurableOfBulkViewSet.as_view({'get':'list'})
product_configurable_of_bulk_detail = ProductConfigurableOfBulkViewSet.as_view({'get':'retrieve','delete':'destroy'})

class ProductConfigurableOfMultipleViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductConfigurableOfMultiple
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductConfigurableOfMultipleSerializer

product_configurable_of_multiple_list = ProductConfigurableOfMultipleViewSet.as_view({'get':'list'})
product_configurable_of_multiple_detail = ProductConfigurableOfMultipleViewSet.as_view({'get':'retrieve','delete':'destroy'})



## EAV viewset

class ProductIntEavViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductIntEav
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductIntEavSerializer

product_int_eav_list = ProductIntEavViewSet.as_view({'get':'list'})
product_int_eav_detail = ProductIntEavViewSet.as_view({'get':'retrieve'})

class ProductBooleanEavViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductBooleanEav
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductBooleanEavSerializer

product_boolean_eav_list = ProductBooleanEavViewSet.as_view({'get':'list'})
product_boolean_eav_detail = ProductBooleanEavViewSet.as_view({'get':'retrieve'})

class ProductDecimalEavViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductDecimalEav
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductDecimalEavSerializer

product_decimal_eav_list = ProductDecimalEavViewSet.as_view({'get':'list'})
product_decimal_eav_detail = ProductDecimalEavViewSet.as_view({'get':'retrieve'})

class ProductTextEavViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductTextEav
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductTextEavSerializer

product_text_eav_list = ProductTextEavViewSet.as_view({'get':'list'})
product_text_eav_detail = ProductTextEavViewSet.as_view({'get':'retrieve'})

class ProductCharEavViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductCharEav
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductCharEavSerializer

product_char_eav_list = ProductCharEavViewSet.as_view({'get':'list'})
product_char_eav_detail = ProductCharEavViewSet.as_view({'get':'retrieve'})

class ProductUrlEavViewSet(ProductMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = ProductUrlEav
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProductUrlEavSerializer

product_url_eav_list = ProductUrlEavViewSet.as_view({'get':'list'})
product_url_eav_detail = ProductUrlEavViewSet.as_view({'get':'retrieve'})


#Attributi
class AttributeViewSet(CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = Attribute
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = AttributeSerializer

attribute_list = AttributeViewSet.as_view({'get':'list','post':'create'})
attribute_detail = AttributeViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

from pprint import PrettyPrinter

class ProductSave(APIView):
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)

    # Save existing product
    def post(self,request,format=None):
        data={}
        company=Company.objects.get(id=request.GET.get("company"))
        marketplace=Marketplace.objects.get(company=company,id=request.GET.get("marketplace"))
        try:
            data["id"]=request.data["id"]
            data["sku"]=request.data["sku"]
            data["type"]=request.data["type"]
        except Exception as exc:
            raise APIException({"detail": "Errore "+str(exc) })
        for key,val in data.items():
            if val in ["",None]:
                raise APIException({"detail": str(key)+" non può essere nullo" })
        if "title" in request.data:
            data["title"]=request.data["title"]
        if "gtin" in request.data:
            data["gtin"]=request.data["gtin"]
        if "gtin_type" in request.data:
            data["gtin_type"]=request.data["gtin_type"]
        if "gtin_type" in data and data["gtin_type"] not in ["NOGTIN","ISBN","EAN"]:
            raise APIException({"detail": "Tipo GTIN non può essere nullo" })
        if "gtin_type" in data and "gtin" in data and data["gtin_type"]!="NOGTIN" and data["gtin"] in [None,""]:
            raise APIException({"detail": "Nessun GTIN inserito." })
        product=None
        if data["type"]=="S":
            try:
                product=ProductSimple.objects.get(id=data["id"],company=company,sku=data["sku"])
            except:
                raise APIException({"detail": "Il prodotto non esiste o è stato cancellato" })
        elif data["type"]=="C":
            try:
                product=ProductConfigurable.objects.get(id=data["id"],company=company,sku=data["sku"])
            except:
                raise APIException({"detail": "Il prodotto non esiste o è stato cancellato" })
        elif data["type"]=="B":
            try:
                product=ProductBulk.objects.get(id=data["id"],company=company,sku=data["sku"])
            except:
                raise APIException({"detail": "Il prodotto non esiste o è stato cancellato" })
        elif data["type"]=="M":
            try:
                product=ProductMultiple.objects.get(id=data["id"],company=company,sku=data["sku"])
            except:
                raise APIException({"detail": "Il prodotto non esiste o è stato cancellato" })
        else:
            raise APIException({"detail": "Tipo prodotto non consentito!" })
        #Titolo
        
        try:
            if "title" in data and data["title"] != None and data["title"].strip()!="":
                eav=product.char_eav.get(company=company,marketplace=marketplace,sku=data["sku"],attribute="title")
                eav.value=data["title"]
                eav.save()
        except:
            raise APIException({"detail": "Non trovo il titolo" })
        

        for attribute in request.data.keys()-data.keys():
            value=request.data[attribute]
            
                
            if attribute=="images":
                for image_number,image_value in value.items():
                    
                    if image_value == None:
                        
                        try:
                            eav=product.url_eav.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=image_number)
                            eav.delete()
                            os.remove(os.path.join(settings.PUBLIC_DIR,company.vid,"products",data["sku"],str(marketplace.code)+"_"+str(marketplace.country)+"_"+str(marketplace.id),image_number+".jpg"))
                        except:
                            continue
                        
                    else:
                        image_file_path=os.path.join(settings.PUBLIC_DIR,company.vid,"products",data["sku"],str(marketplace.code)+"_"+str(marketplace.country)+"_"+str(marketplace.id))
                        image_data = re.sub('^data:image/.+;base64,', '', image_value)
                        image = Image.open(BytesIO(base64.b64decode(image_data))).convert("RGB")
                        imageout=image.resize((2000,2000))
                        if not os.path.exists(image_file_path):
                            os.makedirs(image_file_path,exist_ok=True)
                        imageout.save(os.path.join(image_file_path,image_number+".jpg"),format="jpeg")
                        url=os.path.join("/share",company.vid,"products",data["sku"],str(marketplace.code)+"_"+str(marketplace.country)+"_"+str(marketplace.id),image_number+".jpg")
                        try:
                            eav=product.url_eav.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=image_number)
                            eav.value=url
                            eav.save()
                        except:
                            eav=ProductUrlEav(company=company,marketplace=marketplace,sku=data["sku"],attribute=image_number,value=url)
                            eav.save()
                            product.url_eav.add(eav)
                            product.save()
                    # except:
                    #     pass
                    
            else:
                try:
                    typeObj=Attribute.objects.get(company=company,name=attribute).type
                    try:
                        eav=None
                        if typeObj == "CHAR":
                            eav=ProductCharEav.objects.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute)
                        elif typeObj == "TEXT":
                            eav=ProductTextEav.objects.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute)
                        elif typeObj == "BOOLEAN":
                            eav=ProductBooleanEav.objects.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute)
                        elif typeObj == "INT":
                            eav=ProductIntEav.objects.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute)
                        elif typeObj == "DECIMAL":
                            eav=ProductDecimalEav.objects.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute)
                        elif typeObj == "URL":
                            eav=ProductUrlEav.objects.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute)
                        
                        if value == None or value.strip()=="":
                            eav.delete()
                        else:
                            eav.value=value
                            eav.save()
                            #recheck
                            try:
                                if typeObj == "CHAR":
                                    product.char_eav.add(eav)
                                elif typeObj == "TEXT":
                                    product.text_eav.add(eav)
                                elif typeObj == "BOOLEAN":
                                    product.boolean_eav.add(eav)
                                elif typeObj == "INT":
                                    product.int_eav.add(eav)
                                elif typeObj == "DECIMAL":
                                    product.decimal_eav.add(eav)
                                elif typeObj == "URL":
                                    product.url_eav.add(eav)
                            except:
                                pass
                            
                            
                    except:
                        if value != None and value.strip()!="":
                            eav=None
                            if typeObj == "CHAR":
                                eav=ProductCharEav(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute,value=value)
                            elif typeObj == "TEXT":
                                eav=ProductTextEav(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute,value=value)
                            elif typeObj == "BOOLEAN":
                                eav=ProductBooleanEav(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute,value=value)
                            elif typeObj == "INT":
                                eav=ProductIntEav(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute,value=value)
                            elif typeObj == "DECIMAL":
                                eav=ProductDecimalEav(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute,value=value)
                            elif typeObj == "URL":
                                eav=ProductUrlEav(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute,value=value)
                            
                            eav.save()
                            product.char_eav.add(eav)
                            product.save()
                except:
                    continue

        
        
            


        return Response({"results":"Product saved"})
    
    # Create product
    def put(self,request,format=None):
        data={}
        company=Company.objects.get(id=request.GET.get("company"))
        marketplace=Marketplace.objects.get(company=company,id=request.GET.get("marketplace"))
        try:
            data["sku"]=request.data["sku"]
            data["type"]=request.data["type"]
            data["title"]=request.data["title"]
        except Exception as exc:
            raise APIException({"detail": "Errore "+str(exc) })
        for key,val in data.items():
            if val in ["",None]:
                raise APIException({"detail": str(key)+" non può essere nullo" })
        
        data["gtin"]=request.data["gtin"]
        data["gtin_type"]=request.data["gtin_type"]
        if data["gtin_type"] not in ["NOGTIN","ISBN","EAN"]:
            raise APIException({"detail": "Tipo GTIN non può essere nullo" })
        if data["gtin_type"]!="NOGTIN" and data["gtin"] in [None,""]:
            raise APIException({"detail": "Nessun GTIN inserito." })
        product=None
        if data["type"]=="S":
            try:
                product=ProductSimple.objects.get(id=data["id"],company=company,sku=data["sku"])
            except:
                raise APIException({"detail": "Il prodotto non esiste o è stato cancellato" })
        elif data["type"]=="C":
            try:
                product=ProductConfigurable.objects.get(id=data["id"],company=company,sku=data["sku"])
            except:
                raise APIException({"detail": "Il prodotto non esiste o è stato cancellato" })
        elif data["type"]=="B":
            try:
                product=ProductBulk.objects.get(id=data["id"],company=company,sku=data["sku"])
            except:
                raise APIException({"detail": "Il prodotto non esiste o è stato cancellato" })
        elif data["type"]=="M":
            try:
                product=ProductMultiple.objects.get(id=data["id"],company=company,sku=data["sku"])
            except:
                raise APIException({"detail": "Il prodotto non esiste o è stato cancellato" })
        else:
            raise APIException({"detail": "Tipo prodotto non consentito!" })
        #Titolo
        
        try:
            if "title" in data and data["title"] != None and data["title"].strip()!="":
                eav=product.char_eav.get(company=company,marketplace=marketplace,sku=data["sku"],attribute="title")
                eav.value=data["title"]
                eav.save()
        except:
            raise APIException({"detail": "Non trovo il titolo" })
        

        for attribute in request.data.keys()-data.keys():
            value=request.data[attribute]
            
                
            if attribute=="images":
                for image_number,image_value in value.items():
                    
                    if image_value == None:
                        
                        try:
                            eav=product.url_eav.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=image_number)
                            eav.delete()
                            os.remove(os.path.join(settings.PUBLIC_DIR,company.vid,"products",data["sku"],str(marketplace.code)+"_"+str(marketplace.country)+"_"+str(marketplace.id),image_number+".jpg"))
                        except:
                            continue
                        
                    else:
                        image_file_path=os.path.join(settings.PUBLIC_DIR,company.vid,"products",data["sku"],str(marketplace.code)+"_"+str(marketplace.country)+"_"+str(marketplace.id))
                        image_data = re.sub('^data:image/.+;base64,', '', image_value)
                        image = Image.open(BytesIO(base64.b64decode(image_data))).convert("RGB")
                        imageout=image.resize((2000,2000))
                        if not os.path.exists(image_file_path):
                            os.makedirs(image_file_path,exist_ok=True)
                        imageout.save(os.path.join(image_file_path,image_number+".jpg"),format="jpeg")
                        url=os.path.join("/share",company.vid,"products",data["sku"],str(marketplace.code)+"_"+str(marketplace.country)+"_"+str(marketplace.id),image_number+".jpg")
                        try:
                            eav=product.url_eav.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=image_number)
                            eav.value=url
                            eav.save()
                        except:
                            eav=ProductUrlEav(company=company,marketplace=marketplace,sku=data["sku"],attribute=image_number,value=url)
                            eav.save()
                            product.url_eav.add(eav)
                            product.save()
                    # except:
                    #     pass
                    
            else:
                try:
                    typeObj=Attribute.objects.get(company=company,name=attribute).type
                    try:
                        eav=None
                        if typeObj == "CHAR":
                            eav=ProductCharEav.objects.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute)
                        elif typeObj == "TEXT":
                            eav=ProductTextEav.objects.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute)
                        elif typeObj == "BOOLEAN":
                            eav=ProductBooleanEav.objects.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute)
                        elif typeObj == "INT":
                            eav=ProductIntEav.objects.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute)
                        elif typeObj == "DECIMAL":
                            eav=ProductDecimalEav.objects.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute)
                        elif typeObj == "URL":
                            eav=ProductUrlEav.objects.get(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute)
                        
                        if value == None or value.strip()=="":
                            eav.delete()
                        else:
                            eav.value=value
                            eav.save()
                    except:
                        if value != None and value.strip()!="":
                            eav=None
                            if typeObj == "CHAR":
                                eav=ProductCharEav(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute,value=value)
                            elif typeObj == "TEXT":
                                eav=ProductTextEav(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute,value=value)
                            elif typeObj == "BOOLEAN":
                                eav=ProductBooleanEav(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute,value=value)
                            elif typeObj == "INT":
                                eav=ProductIntEav(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute,value=value)
                            elif typeObj == "DECIMAL":
                                eav=ProductDecimalEav(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute,value=value)
                            elif typeObj == "URL":
                                eav=ProductUrlEav(company=company,marketplace=marketplace,sku=data["sku"],attribute=attribute,value=value)
                            
                            eav.save()
                            product.char_eav.add(eav)
                            product.save()
                except:
                    continue

        
        
            


        return Response({"results":"Product saved"})


class ProductDelete(APIView):
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    def post(self,request):
        company=Company.objects.get(id=request.GET.get("company"))
        marketplace=None
        try:
            marketplace=Marketplace.objects.get(id=request.GET.get("marketplace"),company=company)
        except:
            pass
        if request.GET.get("type")=="S":
            print(request.data)
            objs=ProductSimple.objects.filter(id__in=request.data.keys(),company=company)
            if marketplace is not None:
                for obj in objs:
                    for objeav in obj.char_eav.filter(company=company,marketplace=marketplace,sku=obj.sku):
                        objeav.delete()
                    for objeav in obj.url_eav.filter(company=company,marketplace=marketplace,sku=obj.sku):
                        if "image" in objeav.attribute[:5]:
                            try:
                                os.remove(os.path.join(settings.PUBLIC_DIR,company.vid,"products",obj.sku,str(objeav.marketplace.code)+"_"+str(objeav.marketplace.country)+"_"+str(objeav.marketplace.id),objeav.attribute+".jpg"))
                            except:
                                pass
                        objeav.delete()
                    for objeav in obj.text_eav.filter(company=company,marketplace=marketplace,sku=obj.sku):
                        objeav.delete()
                    for objeav in obj.int_eav.filter(company=company,marketplace=marketplace,sku=obj.sku):
                        objeav.delete()
                    for objeav in obj.decimal_eav.filter(company=company,marketplace=marketplace,sku=obj.sku):
                        objeav.delete()
                    for objeav in obj.boolean_eav.filter(company=company,marketplace=marketplace,sku=obj.sku):
                        objeav.delete()
            else:
                for obj in objs:
                    for objeav in obj.char_eav.filter(company=company,sku=obj.sku):
                        objeav.delete()
                    for objeav in obj.url_eav.filter(company=company,sku=obj.sku):
                        if "image" in objeav.attribute[:5]:
                            try:
                                os.remove(os.path.join(settings.PUBLIC_DIR,company.vid,"products",obj.sku,str(objeav.marketplace.code)+"_"+str(objeav.marketplace.country)+"_"+str(objeav.marketplace.id),objeav.attribute+".jpg"))
                            except:
                                pass
                        objeav.delete()
                    for objeav in obj.text_eav.filter(company=company,sku=obj.sku):
                        objeav.delete()
                    for objeav in obj.int_eav.filter(company=company,sku=obj.sku):
                        objeav.delete()
                    for objeav in obj.decimal_eav.filter(company=company,sku=obj.sku):
                        objeav.delete()
                    for objeav in obj.boolean_eav.filter(company=company,sku=obj.sku):
                        objeav.delete()
                    obj.delete()

        


        
        return Response({"results":"Products deleted"})


class AbstractProductsListView(APIView):
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    def get(self,request,format=None):
        
        results=[]
        for obj in ProductSimple.objects.filter(company=request.GET.get("company")):
            try:
                title=obj.char_eav.get(sku=obj.sku,company=request.GET.get("company"),marketplace=request.GET.get("marketplace"),attribute="title").value
                results.append({"title":title,"sku":obj.sku,"type":"S","id":obj.id})
            except:
                pass
        for obj in ProductConfigurable.objects.filter(company=request.GET.get("company")):
            try:
                title=obj.char_eav.get(sku=obj.sku,company=request.GET.get("company"),marketplace=request.GET.get("marketplace"),attribute="title").value
                results.append({"title":title,"sku":obj.sku,"type":"C","id":obj.id})
            except:
                pass
        for obj in ProductMultiple.objects.filter(company=request.GET.get("company")):
            try:
                title=obj.char_eav.get(sku=obj.sku,company=request.GET.get("company"),marketplace=request.GET.get("marketplace"),attribute="title").value
                results.append({"title":title,"sku":obj.sku,"type":"M","id":obj.id})
            except:
                pass
        for obj in ProductBulk.objects.filter(company=request.GET.get("company")):
            try:
                title=obj.char_eav.get(sku=obj.sku,company=request.GET.get("company"),marketplace=request.GET.get("marketplace"),attribute="title").value
                results.append({"title":title,"sku":obj.sku,"type":"B","id":obj.id})
            except:
                pass
            
            
        return Response({"results":  results} )


class AbstractVariationsView(APIView):

    def get(self,request):
        childs_available=set()
        childs_selected=[]
        variations_available=set()
        variations_selected=[]

        abstract_products=[]
        try:
            company=Company.objects.get(id=request.GET.get("company"))
            marketplace=Marketplace.objects.get(company=company,id=request.GET.get("marketplace"))

            simpleQueryset=ProductSimple.objects.filter(company=company)
            multipleQueryset=ProductMultiple.objects.filter(company=company)
            bulkQueryset=ProductBulk.objects.filter(company=company)
        except:
            raise PermissionDenied(detail="Ditta errata!")

        if request.GET.get("childs") not in ["",None,"null"]:
            childs_selected=request.GET.get("childs").split(",")
        if request.GET.get("variations") not in ["",None,"null"]:
            variations_selected=request.GET.get("variations").split(",")
        
        #childs_selected=["PLEXTOPA1-ORO"]
        
        attributes=set(Attribute.objects.filter(company=company,classification="O").values_list('name',flat=True))
        attributes_decimal=ProductDecimalEav.objects.filter(company=company,marketplace=marketplace,attribute__in=list(attributes))
        attributes_char=ProductCharEav.objects.filter(company=company,marketplace=marketplace,attribute__in=list(attributes))
        attributes_int=ProductIntEav.objects.filter(company=company,marketplace=marketplace,attribute__in=list(attributes))
        if len(childs_selected)==0 and len(variations_selected)==0:
            variations_available=set(attributes_decimal.values_list("attribute",flat=True)).union(set(attributes_char.values_list("attribute",flat=True))).union(set(attributes_int.values_list("attribute",flat=True)))
            childs_available=set(attributes_decimal.values_list("sku",flat=True)).union(set(attributes_char.values_list("sku",flat=True))).union(set(attributes_int.values_list("sku",flat=True)))
            
        elif len(childs_selected) > 0 and len(variations_selected) == 0:
                # prendo gli attributi selezionati
                # vedo quali sku hanno gli attributi selezionati e li metto in childs_availables (set)
                # prendo gli attributi degli sku selezionati (intersect) e li metto in variations_availables
            variations_available=set(attributes_decimal.filter(sku__in=childs_selected).values_list("attribute",flat=True)).union(set(attributes_char.filter(sku__in=childs_selected).values_list("attribute",flat=True))).union(set(attributes_int.filter(sku__in=childs_selected).values_list("attribute",flat=True)))
            childs_available=set(attributes_decimal.filter(attribute__in=variations_available).values_list("sku",flat=True)).union(set(attributes_char.filter(attribute__in=variations_available).values_list("sku",flat=True))).union(set(attributes_int.filter(attribute__in=variations_available).values_list("sku",flat=True)))

        elif len(childs_selected) == 0 and len(variations_selected) > 0:
            childs_available=set(attributes_decimal.filter(attribute__in=variations_selected).values_list("sku",flat=True)).union(set(attributes_char.filter(attribute__in=variations_selected).values_list("sku",flat=True))).union(set(attributes_int.filter(attribute__in=variations_selected).values_list("sku",flat=True)))
            variations_available=set(attributes_decimal.filter(sku__in=childs_available).values_list("attribute",flat=True)).union(set(attributes_char.filter(sku__in=childs_available).values_list("attribute",flat=True))).union(set(attributes_int.filter(sku__in=childs_available).values_list("attribute",flat=True)))

        elif len(childs_selected) > 0 and len(variations_selected) > 0:
            variations_available=set(attributes_decimal.filter(sku__in=childs_selected).values_list("attribute",flat=True)).union(set(attributes_char.filter(sku__in=childs_selected).values_list("attribute",flat=True))).union(set(attributes_int.filter(sku__in=childs_selected).values_list("attribute",flat=True)))
            childs_available=set(attributes_decimal.filter(attribute__in=variations_selected).values_list("sku",flat=True)).union(set(attributes_char.filter(attribute__in=variations_selected).values_list("sku",flat=True))).union(set(attributes_int.filter(attribute__in=variations_selected).values_list("sku",flat=True)))

        
        childs_available=list(set(childs_available)-set(childs_selected))
        
        variations_available=list(variations_available-set(variations_selected))
        for sku in childs_available:
            if simpleQueryset.filter(sku=sku).exists():
                obj=simpleQueryset.get(sku=sku)
                title=None
                try:
                    title=obj.char_eav.get(attribute="title",marketplace=marketplace,company=company).value
                except:
                    pass
                abstract_products.append({"id":obj.id,"sku":obj.sku,"title":title})

            elif multipleQueryset.filter(sku=sku).exists():
                obj=multipleQueryset.get(sku=sku)
                title=None
                try:
                    title=obj.char_eav.get(attribute="title",marketplace=request.GET.get("marketplace"),company=company).value
                except:
                    pass
                abstract_products.append({"id":obj.id,"sku":obj.sku,"title":title})
            
            elif bulkQueryset.filter(sku=sku).exists():
                obj=bulkQueryset.get(sku=sku)
                title=None
                try:
                    title=obj.char_eav.get(attribute="title",marketplace=request.GET.get("marketplace"),company=company).value
                except:
                    pass
                abstract_products.append({"id":obj.id,"sku":obj.sku,"title":title})
        results={ "childs_selected": childs_selected ,  "childs_availables" : abstract_products, "variations_selected": variations_selected, "variations_available": variations_available }
        return JsonResponse({"results":  results} )

    # def post(self,request):
    #     language="IT"
    #     vid=None
    #     company=None
    #     childs_available=set()
    #     childs_selected=[]
    #     variations_available=set()
    #     variations_selected=[]
    #     marketplace=None
    #     if request.user.is_staff:
    #         vid=request.POST.get("vid")
    #     else:
    #         vid=UserInfo(user=request.user).vid

    #     if request.POST.get("childs") not in ["",None,"null"]:
    #         childs_selected=request.POST.get("childs").split(",")
    #     if request.POST.get("variations") not in ["",None,"null"]:
    #         variations_selected=request.POST.get("variations").split(",")
    #     if request.POST.get("marketplace") not in ["",None,"null"]:
    #         marketplace=request.POST.get("marketplace")

    #     banned_sku=set(DraftProduct.objects.filter(vid=vid,draftType="C").values_list("sku",flat=True))
    #     banned_sku=banned_sku.union(set(DraftProduct.objects.filter(vid=vid,draftType="B").values_list("sku",flat=True)))
    #     objs=DraftProductEAV.objects.filter(vid=vid,language=language,marketplace=marketplace,attribute="others").exclude(value__in=["{}",""]).exclude(sku__in=banned_sku)

    #     if len(childs_selected) is 0 and len(variations_selected) is 0:
    #         for obj in objs:
    #             try:
    #                 variations_available=variations_available.union(set(dict(json.loads(obj.value)).keys()))
    #             except json.decoder.JSONDecodeError:
    #                 pass
    #         childs_available=set(objs.order_by("sku").values_list("sku",flat=True))
    #     elif len(childs_selected) > 0 and len(variations_selected) is 0:
    #         for sku in childs_selected:
    #             if len(variations_available) is 0:
    #                 variations_available=set(dict(json.loads(objs.get(sku=sku,attribute="others").value)).keys())
    #             else:
    #                 variations_available=variations_available.intersection(set(dict(json.loads(objs.get(sku=sku,attribute="others").value)).keys()))
    #         for obj in objs:
    #             if len(variations_available-set(dict(json.loads(obj.value)).keys())) is 0:
    #                 childs_available.add(obj.sku)

    #     elif len(childs_selected) is 0 and len(variations_selected) > 0:
    #         for obj in objs:
    #             if len(set(variations_selected)-set(dict(json.loads(obj.value)).keys())) is 0:
    #                 childs_available.add(obj.sku)
    #                 if len(variations_available) is 0:
    #                     variations_available = set(dict(json.loads(obj.value)).keys())
    #                 else:
    #                     variations_available = variations_available.intersection(set(dict(json.loads(obj.value)).keys()))
    #     else:
    #         for sku in childs_selected:
    #             if len(variations_available) is 0:
    #                 variations_available=set(dict(json.loads(objs.get(sku=sku,attribute="others").value)).keys())
    #             else:
    #                 variations_available=variations_available.intersection(set(dict(json.loads(objs.get(sku=sku,attribute="others").value)).keys()))
    #         for obj in objs:
    #             if len(variations_available-set(dict(json.loads(obj.value)).keys())) is 0:
    #                 childs_available.add(obj.sku)

    #         for obj in objs:
    #             if len(set(variations_selected)-set(dict(json.loads(obj.value)).keys())) is 0:
    #                 childs_available.add(obj.sku)
    #                 if len(variations_available) is 0:
    #                     variations_available = set(dict(json.loads(obj.value)).keys())
    #                 else:
    #                     variations_available = variations_available.intersection(set(dict(json.loads(obj.value)).keys()))

    #     childs_available=list(set(childs_available)-set(childs_selected))
    #     variations_available=list(variations_available-set(variations_selected))
    #     childs={"availables":childs_available,"selected":childs_selected}
    #     variations={"availables":variations_available,"selected":variations_selected}
    #     response={"childs":childs,"variations":variations}
    #     return JsonResponse(response)


