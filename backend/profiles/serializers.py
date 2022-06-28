from rest_framework import serializers
from .models import Profile

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','password','last_login','is_superuser','username','first_name','last_name','email','is_staff','is_active','date_joined')
        read_only_fields = ('id','password','last_login','date_joined')

    
    

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ('id','phone','user')
        read_only_fields = ('id',)
        depth=1
        
    def create(self,validated_data):
        user_data=validated_data.pop("user")
        user_instance=User.objects.create(**user_data)
        profile=Profile.objects.create(user=user_instance,**validated_data)
        return profile

    def update(self,instance,validated_data):
        user_data=validated_data.pop("user")
        user=User.objects.get(pk=instance.user.id)
        user.is_superuser=user_data["is_superuser"] if "is_superuser" in user_data else user.is_superuser
        user.first_name=user_data["first_name"]
        user.last_name=user_data["last_name"]
        user.email=user_data["email"]
        user.is_staff=user_data["is_staff"] if "is_staff" in user_data else user.is_staff
        user.is_active=user_data["is_active"] if "is_active" in user_data else user.is_active
        user.save()
        instance.user=user
        instance.phone=validated_data.get('phone',instance.phone)
        instance.save()
        return instance