from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_condition import Or,And
from backend.permissions import IsSuperUser,IsVendor,IsStaff,IsVendorReadOnly,IsVendorStaffReadOnly,IsVendorCollaboratorReadOnly
from .serializers import MarketplaceSerializer
from backend.mixins import VendorModelMixin
from .models import Marketplace


class MarketplaceViewSet(VendorModelMixin,viewsets.ModelViewSet):
    model = Marketplace
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendorReadOnly,IsVendorStaffReadOnly,IsVendorCollaboratorReadOnly)),)
    serializer_class = MarketplaceSerializer


marketplace_list = MarketplaceViewSet.as_view({'get':'list','post':'create'})
marketplace_detail = MarketplaceViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

# marketplace_router = DefaultRouter()
# marketplace_router.register(r'marketplaces',MarketplaceViewSet)