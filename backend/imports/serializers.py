from rest_framework import serializers
from .models import Import

class ImportSerializer(serializers.ModelSerializer):
    _ftype=serializers.CharField(source="get_ftype_display",read_only=True)
    _status=serializers.CharField(source="get_status_display",read_only=True)
    _create = serializers.DateTimeField(source="create",format="%d-%m-%Y %H:%M:%S",read_only=True)
        
    class Meta:
        model = Import
        fields = ('id','marketplace','company',"_status","_ftype",'ftype','_create','datasheet','status','messages')
        read_only_fields =('id','_ftype','_status','_create','datasheet','marketplace','status','messages')
        depth=0


    

   
    
    