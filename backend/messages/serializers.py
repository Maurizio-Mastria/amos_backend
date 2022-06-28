from rest_framework import serializers
from .models import InboxMessage,OutboxMessage



class InboxMessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InboxMessage
        fields = ('id','text','address')
        read_only_fields =('id','text','address')


class OutboxMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutboxMessage
        fields = ('id','text','address')
        read_only_fields =('id','text','address')

class MessageSerializer(serializers.ModelSerializer):
    inbox=InboxMessageSerializer(many=True)
    outbox=OutboxMessageSerializer(many=True)
    class Meta:
        model = OutboxMessage
        fields = '__all__'
        read_only_fields =('id','company','marketplace','inbox','outbox')