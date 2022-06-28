from rest_framework.exceptions import APIException,PermissionDenied
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_condition import Or,And
from backend.permissions import IsSuperUser,IsStaff,IsVendorReadOnly,IsVendorStaffReadOnly,IsVendorCollaboratorReadOnly
from .serializers import CompanySerializer

from .models import Company
from django.db.utils import IntegrityError


class CompanyMixin(object):
    def get_queryset(self):
        
        if self.request.user.is_superuser or self.request.user.is_staff:
            queryset=self.model.objects.all().order_by("id")
        else:
            company=Company.objects.filter(vendors=self.request.user)|\
                Company.objects.filter(staff=self.request.user)|\
                    Company.objects.filter(collaborators=self.request.user)
            if company.exists():
                print("OK")
                queryset=company.order_by("id")
            else:
                queryset=None
        return queryset

    def perform_create(self,serializer):
        if not self.request.user.is_superuser and not self.request.user.is_staff:
            company=Company.objects.filter(vendors=self.request.user)|\
                Company.objects.filter(staff=self.request.user)|\
                    Company.objects.filter(collaborators=self.request.user)
            try:
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise APIException(detail="Errore!")
            except IntegrityError as exc:
                raise PermissionDenied(detail=exc)
        else:
            try:
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise APIException(detail="Errore!")
            except IntegrityError:
                raise PermissionDenied(detail="%s già esistente" % (self.model._meta.verbose_name.title()))

    def perform_update(self,serializer):
        if not self.request.user.is_superuser and not self.request.user.is_staff:
            company=Company.objects.filter(vendors=self.request.user)|\
                Company.objects.filter(staff=self.request.user)|\
                    Company.objects.filter(collaborators=self.request.user)
            try:
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise APIException(detail="Errore!")
            except IntegrityError as exc:
                raise PermissionDenied(detail=exc)
        else:
            try:
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise APIException(detail="Errore!")
            except IntegrityError:
                raise PermissionDenied(detail="%s già esistente" % (self.model._meta.verbose_name.title()))


class CompanyViewSet(CompanyMixin,viewsets.ModelViewSet):
    model = Company
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendorReadOnly,IsVendorStaffReadOnly,IsVendorCollaboratorReadOnly)),)
    serializer_class = CompanySerializer


company_list = CompanyViewSet.as_view({'get':'list','post':'create'})
company_detail = CompanyViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})