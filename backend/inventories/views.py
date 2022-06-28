from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_condition import Or,And
from backend.permissions import IsSuperUser,IsVendor,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaboratorReadOnly
from .serializers import InventorySerializer
from backend.mixins import VendorModelMixin
from .models import Inventory


class InventoryViewSet(VendorModelMixin,viewsets.ModelViewSet):
    model = Inventory
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaboratorReadOnly)),)
    serializer_class = InventorySerializer


inventory_list = InventoryViewSet.as_view({'get':'list','post':'create'})
inventory_detail = InventoryViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

# marketplace_router = DefaultRouter()
# marketplace_router.register(r'marketplaces',MarketplaceViewSet)