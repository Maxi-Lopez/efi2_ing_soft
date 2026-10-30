from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.permissions import AllowAny
from usuarios.permissions import PermissionVendedor
from rest_framework.decorators import action

from .models import Venta, DetalleVenta
from .serializers import VentaSerializer, VentaGetSerializer, DetalleVentaSerializer


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = VentaSerializer


    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [PermissionVendedor]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def eliminado_logico(self, request, pk=None):
        venta = self.get_object()
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        venta.is_active = False
        venta.nro_factura = f'delete-{venta.nro_factura}-{timestamp}' if venta.nro_factura else f'delete-{timestamp}'
        venta.save()
        return Response(
            {'detail': 'La venta se elimino correctamente'},
            status=status.HTTP_200_OK
        )


class VentaGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Venta.objects.filter(is_active=True).select_related('cliente').prefetch_related('detalles__producto__marca', 'detalles__producto__categoria').order_by('-created_at')
    serializer_class = VentaGetSerializer
    permission_classes = [AllowAny]


class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = DetalleVentaSerializer

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
            {'detail': 'El detalle de venta se elimino correctamente'},
            status=status.HTTP_200_OK
        )


class DetalleVentaGetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DetalleVenta.objects.filter(is_active=True).select_related('venta', 'producto').order_by('-created_at')
    serializer_class = DetalleVentaSerializer
    permission_classes = [AllowAny]
