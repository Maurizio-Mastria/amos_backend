from rest_framework import serializers
from .models import Company, Authorization
from django.contrib.auth.models import User
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email','last_login','is_active','profile')
        read_only_fields = ('id','username','first_name','last_name','email','last_login','is_active','profile')
        depth=1

class AuthorizationSerializer(serializers.ModelSerializer):
    user=AuthUserSerializer()
    class Meta:
        model = Authorization
        fields = ('id','application','permission','user')
        read_only_fields=('application','user')


class AuthorizationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authorization
        exclude = ('user',)
        
        