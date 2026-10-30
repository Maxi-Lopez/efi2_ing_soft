from rest_framework import serializers
from .models import Venta, DetalleVenta
from catalogo.serializers import ProductoListSerializer
from usuarios.serializers import UsuarioPublicSerializer


class DetalleVentaSerializer(serializers.ModelSerializer):
    producto = ProductoListSerializer(read_only=True)

    class Meta:
        model = DetalleVenta
        fields = [
            'id', 'venta', 'producto', 'unidades', 'precio_unitario',
            'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'is_active']


class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = [
            'id', 'cliente', 'estado', 'nro_factura',
            'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'is_active']


class VentaGetSerializer(VentaSerializer):
    cliente = UsuarioPublicSerializer(read_only=True)
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta(VentaSerializer.Meta):
        fields = VentaSerializer.Meta.fields + ['cliente', 'detalles', 'total']

    def get_total(self, obj):
        return sum(detalle.unidades * float(detalle.precio_unitario) for detalle in obj.detalles.all())
