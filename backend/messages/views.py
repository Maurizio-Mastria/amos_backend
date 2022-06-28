from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_condition import Or,And
from backend.permissions import IsSuperUser,IsVendor,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator
from .serializers import MessageSerializer
from backend.mixins import VendorModelMixin
from .models import Message


class MessageViewSet(VendorModelMixin,viewsets.ModelViewSet):
    model = Message
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = MessageSerializer


message_list = MessageViewSet.as_view({'get':'list','post':'create'})
message_detail = MessageViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

# marketplace_router = DefaultRouter()
# marketplace_router.register(r'marketplaces',MarketplaceViewSet)