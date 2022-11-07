from pprint import PrettyPrinter
from rest_framework.exceptions import APIException,PermissionDenied
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from companies.models import Company
from profiles.models import Profile
from rest_framework import serializers
from django.contrib.auth.models import User
from django.http.response import JsonResponse
import json


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [field.name for field in User._meta.fields]+['profile']
        depth=1


class UserFilterMixin(object):
    def get_queryset(self):
        #se superuser ... tutti
        #se staff tutti
        queryset=User.objects.all()
            

            
        return queryset
        


class UserViewSet(UserFilterMixin,viewsets.ModelViewSet):
    model = User
    permission_class = IsAuthenticated
    serializer_class = UserSerializer



class UserMeMixin(object):
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id).order_by("id")

            
        
class UserMeViewSet(UserMeMixin,viewsets.ModelViewSet):
    model = User
    permission_class = IsAuthenticated
    serializer_class = UserSerializer


user_list = UserViewSet.as_view({'get':'list',})
user_detail = UserViewSet.as_view({'get':'retrieve','put':'partial_update'})
user_me_detail = UserMeViewSet.as_view({'get':'list'})