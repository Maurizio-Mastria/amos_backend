from pprint import PrettyPrinter
from rest_framework.exceptions import APIException,PermissionDenied
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_condition import Or,And
from backend.permissions import IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator
from .serializers import ProfileSerializer
from companies.models import Company
from profiles.models import Profile
from django.db.utils import IntegrityError
from rest_framework.response import Response






class ProfileMixin(object):
    def get_queryset(self):
        
        if self.request.user.is_superuser or self.request.user.is_staff:
            queryset=self.model.objects.all().order_by("id")
        else:
            queryset=self.model.objects.none()
            if Company.objects.filter(vendors=self.request.user).exists():
                users=Company.objects.filter(vendors=self.request.user)[0].vendors.all()|\
                    Company.objects.filter(vendors=self.request.user)[0].staff.all()\
                        |Company.objects.filter(vendors=self.request.user)[0].collaborators.all()
                for obj in users:
                    queryset=queryset|Profile.objects.filter(user=obj)
            elif Company.objects.filter(staff=self.request.user).exists():
                users=Company.objects.filter(staff=self.request.user)[0].staff.filter(id=self.request.user.id)|\
                        Company.objects.filter(staff=self.request.user)[0].collaborators.all()
                for obj in users:
                    queryset=queryset|Profile.objects.filter(user=obj)
            elif Company.objects.filter(collaborators=self.request.user).exists():
                users=Company.objects.filter(collaborators=self.request.user)[0].collaborators.filter(id=self.request.user.id)
                for obj in users:
                    queryset=queryset|Profile.objects.filter(user=obj)
            else:
                queryset=None
        pp=PrettyPrinter()
        pp.pprint(queryset)
        return queryset

    def perform_create(self,serializer):
        if not self.request.user.is_superuser and not self.request.user.is_staff:
            company=Company.objects.filter(vendors=self.request.user)|\
                Company.objects.filter(staff=self.request.user)
            if company.exists():
                try:
                    serializer.validated_data["user"]["is_superuser"]=False
                    serializer.validated_data["user"]["is_staff"]=False
                    serializer.validated_data["user"]["is_active"]=True
                    if serializer.is_valid():
                        serializer.save()
                        company[0].collaborators.add(serializer.data['user']["id"])
                    else:
                        raise APIException(detail="Errore!")
                except IntegrityError as exc:
                    raise PermissionDenied(detail=exc)
            else:
                raise PermissionDenied(detail="Non hai l'autorizzazione")
        else:
            try:
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise APIException(detail="Errore!")
            except IntegrityError as exc:
                raise PermissionDenied(detail="%s già esistente! %s"  % (self.model._meta.verbose_name.title(),exc))

    def perform_update(self,serializer):
        if not self.request.user.is_superuser and not self.request.user.is_staff:
            company=Company.objects.filter(vendors=self.request.user)|\
                Company.objects.filter(staff=self.request.user)
            if company.exists():
                try:
                    if "username" in serializer.validated_data["user"]: serializer.validated_data["user"].pop("username")
                    serializer.validated_data["user"]["is_superuser"]=False
                    serializer.validated_data["user"]["is_staff"]=False
                    if "is_active" in serializer.validated_data["user"]: serializer.validated_data["user"].pop("is_active")
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise APIException(detail="Errore!")
                except IntegrityError as exc:
                    raise PermissionDenied(detail=exc)
            else:
                raise PermissionDenied(detail="Non hai l'autorizzazione")
        elif self.request.user.is_staff:
            try:
                if "username" in serializer.validated_data["user"]: serializer.validated_data["user"].pop("username")
                if "is_superuser" in serializer.validated_data["user"]: serializer.validated_data["user"].pop("is_superuser")
                if "is_staff" in serializer.validated_data["user"]: serializer.validated_data["user"].pop("is_staff")
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise APIException(detail="Errore!")
            except IntegrityError as exc:
                raise PermissionDenied(detail="%s già esistente! %s"  % (self.model._meta.verbose_name.title(),exc))
        elif self.request.user.is_superuser:
            try:
                if "username" in serializer.validated_data["user"]: serializer.validated_data["user"].pop("username")
                if "is_superuser" in serializer.validated_data["user"]: serializer.validated_data["user"].pop("is_superuser")
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise APIException(detail="Errore!")
            except IntegrityError as exc:
                raise PermissionDenied(detail="%s già esistente! %s"  % (self.model._meta.verbose_name.title(),exc))

class UserViewSet(ProfileMixin,viewsets.ModelViewSet):
    model = Profile
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ProfileSerializer


user_list = UserViewSet.as_view({'get':'list','post':'create'})
user_detail = UserViewSet.as_view({'get':'retrieve','put':'partial_update','delete':'destroy'})

# marketplace_router = DefaultRouter()
# marketplace_router.register(r'marketplaces',MarketplaceViewSet)