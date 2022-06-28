from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_condition import Or,And
from backend.permissions import IsSuperUser,IsStaff,IsVendorObject,IsVendorStaffObject,IsVendorCollaboratorObject
from .serializers import ImportSerializer
from .mixins import ImportMixin,ImportFileMixin
from backend.mixins import CompanyModelMixin,GenericModelMixin
from .models import Import
from rest_framework.parsers import MultiPartParser



class ImportViewSet(ImportMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = Import
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendorObject,IsVendorStaffObject,IsVendorCollaboratorObject)),)
    serializer_class = ImportSerializer
    parser_classes= (MultiPartParser,)

class ImportUpdateViewSet(ImportMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = Import
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendorObject,IsVendorStaffObject,IsVendorCollaboratorObject)),)
    serializer_class = ImportSerializer
    
class ImportFileViewSet(ImportFileMixin,CompanyModelMixin,GenericModelMixin,viewsets.ModelViewSet):
    model = Import
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendorObject,IsVendorStaffObject,IsVendorCollaboratorObject)),)
    

import_list = ImportViewSet.as_view({'get':'list','post':'create'})
import_detail = ImportUpdateViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})
import_file = ImportFileViewSet.as_view({'get':'retrieve'})