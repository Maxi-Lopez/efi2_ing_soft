from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import AllowAny
from usuarios.permissions import PermissionVendedor
from rest_framework.decorators import action

from .models import Compra, DetalleCompra
from .serializers import CompraSerializer, DetalleCompraSerializer, CompraListSerializer


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = CompraSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [PermissionVendedor]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def eliminado_logico(self, request, pk=None):
        compra = self.get_object()
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        compra.is_active = False
        compra.nro_factura = f'delete-{compra.nro_factura}-{timestamp}' if compra.nro_factura else f'delete-{timestamp}'
        compra.save()
        return Response(
            {'detail': 'La compra se elimino correctamente'},
            status=status.HTTP_200_OK
        )


class CompraGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Compra.objects.filter(is_active=True).select_related('proveedor').order_by('-created_at')
    serializer_class = CompraListSerializer
    permission_classes = [AllowAny]


class CompraListGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Compra.objects.filter(is_active=True).select_related('proveedor').prefetch_related('detalles').order_by('-created_at')
    serializer_class = CompraListSerializer
    permission_classes = [AllowAny]


class DetalleCompraViewSet(viewsets.ModelViewSet):
    queryset = DetalleCompra.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = DetalleCompraSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [PermissionVendedor]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def eliminado_logico(self, request, pk=None):
        detalle = self.get_object()
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        detalle.is_active = False
        detalle.save()
        return Response(
            {'detail': 'El detalle de compra se elimino correctamente'},
            status=status.HTTP_200_OK
        )


class DetalleCompraGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DetalleCompra.objects.filter(is_active=True).select_related('compra', 'producto').order_by('-created_at')
    serializer_class = DetalleCompraSerializer
    permission_classes = [AllowAny]
