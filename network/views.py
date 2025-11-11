from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkNode, Product
from .serializers import NetworkNodeSerializer, ProductSerializer
from .permissions import IsActiveStaffEmployee


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.select_related('supplier').prefetch_related('products').all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveStaffEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country']

    # запрет на изменение debt через API, если в request.data есть debt
    def perform_update(self, serializer):
        data = serializer.validated_data.copy()
        if 'debt' in data:
            data.pop('debt', None)
        serializer.save(**data)

    def partial_update(self, request, *args, **kwargs):
        mutate_data = request.data.copy()
        mutate_data.pop('debt', None)
        request._full_data = mutate_data
        return super().partial_update(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('node').all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveStaffEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['node__country', 'node__city', 'release_date']
