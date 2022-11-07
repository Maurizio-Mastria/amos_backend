from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSimpleSerializer,ProductMultipleSerializer,ProductConfigurableSerializer,ProductBulkSerializer
from .serializers import ProductIntEavSerializer,ProductCharEavSerializer,ProductDecimalEavSerializer,ProductBooleanEavSerializer,ProductTextEavSerializer,ProductUrlEavSerializer
from .serializers import CustomAttributeSerializer,AttributeSerializer,DefaultAttributeSerializer,CategorySerializer
from .mixins import ProductAttributeViewMixin, ProductSimpleViewMixin,CategoryViewMixin,CustomAttributeViewMixin,CategorySimplifyViewMixin
from backend.mixins import AuthorizationMixin
from .models import ProductSimple,ProductMultiple,ProductBulk,ProductConfigurable
# from .models import ProductBulkOfMultiple,ProductBulkOfBulk
# from .models import ProductMultipleOfBulk,ProductMultipleOfMultiple
# from .models import ProductConfigurableOfMultiple,ProductConfigurableOfBulk
# from .serializers import ProductBulkOfBulkSerializer,ProductBulkOfMultipleSerializer,ProductMultipleOfBulkSerializer,ProductMultipleOfMultipleSerializer
# from .serializers import ProductConfigurableOfBulkSerializer,ProductConfigurableOfMultipleSerializer
from .models import ProductBooleanEav,ProductCharEav,ProductIntEav,ProductTextEav,ProductDecimalEav,ProductUrlEav
from .models import Attribute,DefaultAttribute,CustomAttribute,Category
from companies.models import Company
from marketplaces.models import Marketplace
from rest_framework.exceptions import APIException,PermissionDenied
from PIL import Image
import shutil
import re
import base64
from io import BytesIO
import os
# Create your views here.

class CustomAttributeViewSet(CustomAttributeViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = CustomAttribute
    permission_class = IsAuthenticated
    serializer_class = CustomAttributeSerializer

custom_attributes_list = CustomAttributeViewSet.as_view({'get':'list','post':'create'})
custom_attribute_detail = CustomAttributeViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

class AttributeViewSet(ProductAttributeViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Attribute
    permission_class = IsAuthenticated
    serializer_class = AttributeSerializer

attributes_list = AttributeViewSet.as_view({'get':'list','post':'create'})
attribute_detail = AttributeViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

class CategoryViewSet(CategoryViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Category
    permission_class = IsAuthenticated
    serializer_class = CategorySerializer

categories_list = CategoryViewSet.as_view({'get':'list','post':'create'})
category_detail = CategoryViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

class CategorySimplifyViewSet(CategorySimplifyViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Category
    permission_class = IsAuthenticated
    serializer_class = CategorySerializer

categories_simplify_list = CategorySimplifyViewSet.as_view({'get':'list'})

class ProductSimpleViewSet(ProductSimpleViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductSimple
    permission_class = IsAuthenticated
    serializer_class = ProductSimpleSerializer

product_simple_list = ProductSimpleViewSet.as_view({'get':'list','post':'create'})
product_simple_detail = ProductSimpleViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

# class ProductMultipleViewSet(ProductMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = ProductMultiple
#     permission_classes = IsAuthenticated
#     serializer_class = ProductMultipleSerializer

# product_multiple_list = ProductMultipleViewSet.as_view({'get':'list'})
# product_multiple_detail = ProductMultipleViewSet.as_view({'get':'retrieve','delete':'destroy'})

# class ProductBulkViewSet(ProductMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = ProductBulk
#     permission_classes = IsAuthenticated
#     serializer_class = ProductBulkSerializer

# product_bulk_list = ProductBulkViewSet.as_view({'get':'list'})
# product_bulk_detail = ProductBulkViewSet.as_view({'get':'retrieve','delete':'destroy'})

# class ProductConfigurableViewSet(ProductMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = ProductConfigurable
#     permission_classes = IsAuthenticated
#     serializer_class = ProductConfigurableSerializer

# product_configurable_list = ProductConfigurableViewSet.as_view({'get':'list'})
# product_configurable_detail = ProductConfigurableViewSet.as_view({'get':'retrieve','delete':'destroy'})

# class ProductBulkOfBulkViewSet(ProductMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = ProductBulkOfBulk
#     permission_classes = IsAuthenticated
#     serializer_class = ProductBulkOfBulkSerializer

# product_bulk_of_bulk_list = ProductBulkOfBulkViewSet.as_view({'get':'list'})
# product_bulk_of_bulk_detail = ProductBulkOfBulkViewSet.as_view({'get':'retrieve','delete':'destroy'})

# class ProductBulkOfMultipleViewSet(ProductMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = ProductBulkOfMultiple
#     permission_classes = IsAuthenticated
#     serializer_class = ProductBulkOfMultipleSerializer

# product_bulk_of_multiple_list = ProductBulkOfMultipleViewSet.as_view({'get':'list'})
# product_bulk_of_multiple_detail = ProductBulkOfMultipleViewSet.as_view({'get':'retrieve','delete':'destroy'})

# class ProductMultipleOfBulkViewSet(ProductMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = ProductMultipleOfBulk
#     permission_classes = IsAuthenticated
#     serializer_class = ProductMultipleOfBulkSerializer

# product_multiple_of_bulk_list = ProductMultipleOfBulkViewSet.as_view({'get':'list'})
# product_multiple_of_bulk_detail = ProductMultipleOfBulkViewSet.as_view({'get':'retrieve','delete':'destroy'})

# class ProductMultipleOfMultipleViewSet(ProductMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = ProductMultipleOfMultiple
#     permission_classes = IsAuthenticated
#     serializer_class = ProductMultipleOfMultipleSerializer

# product_multiple_of_multiple_list = ProductMultipleOfMultipleViewSet.as_view({'get':'list'})
# product_multiple_of_multiple_detail = ProductMultipleOfMultipleViewSet.as_view({'get':'retrieve','delete':'destroy'})

# class ProductConfigurableOfBulkViewSet(ProductMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = ProductConfigurableOfBulk
#     permission_classes = IsAuthenticated
#     serializer_class = ProductConfigurableOfBulkSerializer

# product_configurable_of_bulk_list = ProductConfigurableOfBulkViewSet.as_view({'get':'list'})
# product_configurable_of_bulk_detail = ProductConfigurableOfBulkViewSet.as_view({'get':'retrieve','delete':'destroy'})

# class ProductConfigurableOfMultipleViewSet(ProductMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = ProductConfigurableOfMultiple
#     permission_classes = IsAuthenticated
#     serializer_class = ProductConfigurableOfMultipleSerializer

# product_configurable_of_multiple_list = ProductConfigurableOfMultipleViewSet.as_view({'get':'list'})
# product_configurable_of_multiple_detail = ProductConfigurableOfMultipleViewSet.as_view({'get':'retrieve','delete':'destroy'})



