from rest_framework.exceptions import APIException,PermissionDenied
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import CompanySerializer,AuthorizationSerializer,AuthorizationCreateSerializer
from companies.models import Company,Authorization
from backend.mixins import AuthorizationMixin
from django.db.utils import IntegrityError
from django.http.response import JsonResponse
from django.contrib.auth.models import User

class CompanyViewMixin(object):
    
    def get_queryset(self):
        if self.request.user.is_superuser or (self.request.user.is_staff and self.request.method != "DELETE"):
            return self.model.objects.all()
        permission=Authorization.Permissions.DENY
        if self.request.method in ["GET"]:
            permission=Authorization.Permissions.READ
        elif self.request.method in ["PUT"]:
            permission=Authorization.Permissions.MODIFY
        # Prendi solo le compagnie cui l'utente ha un permesso uguale o superiore a quello dato
        companies_id=Authorization.objects.filter(user=self.request.user,application="companies",permission__gte=permission).values_list("company",flat=True)
        return self.model.objects.filter(pk__in=companies_id,active=True).order_by("name")
        
        

    def perform_create(self,serializer):
        if not (self.request.user.is_superuser or self.request.user.is_staff):
            raise PermissionDenied(detail="Permesso negato")
        try:
            if serializer.is_valid():
                serializer.save()
            else:
                raise APIException(detail="Permesso negato o errore dati!")
        except IntegrityError:
            raise PermissionDenied(detail="Permesso negato %s già esistente" % (self.model._meta.verbose_name.title()))
        

    def perform_update(self,serializer):
        try:
            if serializer.is_valid():
                serializer.save()
            else:
                raise APIException(detail="Errore!")
        except IntegrityError:
            raise PermissionDenied(detail="%s già esistente" % (self.model._meta.verbose_name.title()))

    def perform_destroy(self, instance):
        
        instance.delete()
        
        
        
        

    


class CompanyViewSet(CompanyViewMixin,viewsets.ModelViewSet):
    model = Company
    permission_class = IsAuthenticated
    serializer_class = CompanySerializer

company_list = CompanyViewSet.as_view({'get':'list','post':'create'})
company_detail = CompanyViewSet.as_view({'get':'retrieve','put':'partial_update','delete':'destroy'})

#################################################################

        
class AuthorizationViewMixin(object):
    
    def get_queryset(self):
        return super().get_queryset("authorizations").order_by("id")
        

    def perform_update(self,serializer):
        try:
            if serializer.is_valid():
                serializer.save()
            else:
                raise APIException(detail="Errore!")
        except IntegrityError:
            raise PermissionDenied(detail="%s già esistente" % (self.model._meta.verbose_name.title()))


class AuthorizationViewSet(AuthorizationViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Authorization
    permission_class = IsAuthenticated
    serializer_class = AuthorizationSerializer

    
    
authorizations_list = AuthorizationViewSet.as_view({'get':'list'})
authorization_detail = AuthorizationViewSet.as_view({'put':'partial_update'})

class AuthorizationCreateViewMixin(object):
    
    def get_queryset(self):
        return super().get_queryset("authorizations").order_by("id")
        

    def perform_create(self,serializer):
        try:
            if serializer.is_valid():
                serializer.save()
            else:
                raise APIException(detail="Errore!")
        except IntegrityError:
            raise PermissionDenied(detail="%s già esistente" % (self.model._meta.verbose_name.title()))


class AuthorizationCreateViewSet(AuthorizationCreateViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Authorization
    permission_class = IsAuthenticated
    serializer_class = AuthorizationCreateSerializer

auth_create = AuthorizationCreateViewSet.as_view({'post':'create'})


class MyAuthorizationsViewMixin(object):
    
    def list(self,request):
        auth={}
        auth["is_superuser"]=self.request.user.is_superuser
        auth["is_staff"]=self.request.user.is_staff
        auth["permissions"]={}
        for perm in Authorization.objects.filter(company=self.request.GET.get("company"),user=self.request.user):
            auth["permissions"][perm.application]=perm.permission
        return JsonResponse(auth)

class MyAuthorizationsViewSet(MyAuthorizationsViewMixin,viewsets.ModelViewSet):
    model = Authorization
    permission_class = IsAuthenticated
    serializer_class = AuthorizationSerializer
    
my_authorizations_list = MyAuthorizationsViewSet.as_view({'get':'list'})