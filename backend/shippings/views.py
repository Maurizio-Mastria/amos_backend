from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_condition import Or,And
from backend.permissions import IsSuperUser,IsVendor,IsStaff,IsVendor, IsVendorCollaboratorReadOnly, IsVendorReadOnly,IsVendorStaff,IsVendorCollaborator, IsVendorStaffReadOnly
from .serializers import ShippingSerializer,CourierSerializer
from backend.mixins import VendorModelMixin
from .mixins import ShippingMixin
from .models import Shipping,Courier


class ShippingViewSet(ShippingMixin,viewsets.ModelViewSet):
    model = Shipping
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = ShippingSerializer


shipping_list = ShippingViewSet.as_view({'get':'list','post':'create'})
shipping_detail = ShippingViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})


class CourierViewSet(VendorModelMixin,viewsets.ModelViewSet):
    model = Courier
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendorReadOnly,IsVendorStaffReadOnly,IsVendorCollaboratorReadOnly)),)
    serializer_class = CourierSerializer


courier_list = CourierViewSet.as_view({'get':'list','post':'create'})
courier_detail = CourierViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})


# marketplace_router = DefaultRouter()
# marketplace_router.register(r'marketplaces',MarketplaceViewSet)