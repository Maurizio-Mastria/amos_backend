from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_condition import Or,And
from backend.permissions import IsSuperUser,IsVendor,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator
from .serializers import OrderSerializer
from .mixins import OrderMixin
from .models import Order


class OrderViewSet(OrderMixin,viewsets.ModelViewSet):
    model = Order
    permission_classes = (And(IsAuthenticated,Or(IsSuperUser,IsStaff,IsVendor,IsVendorStaff,IsVendorCollaborator)),)
    serializer_class = OrderSerializer


order_list = OrderViewSet.as_view({'get':'list','post':'create'})
order_detail = OrderViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

# marketplace_router = DefaultRouter()
# marketplace_router.register(r'marketplaces',MarketplaceViewSet)
