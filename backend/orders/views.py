from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer

from backend.mixins import AuthorizationMixin
from .models import Order


class OrderViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("orders")
        return queryset.order_by("id")

class OrderViewSet(OrderViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Order
    permission_class = IsAuthenticated
    serializer_class = OrderSerializer


order_list = OrderViewSet.as_view({'get':'list','post':'create'})
order_detail = OrderViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

# marketplace_router = DefaultRouter()
# marketplace_router.register(r'marketplaces',MarketplaceViewSet)
