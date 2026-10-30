from rest_framework import serializers
from .models import Compra, DetalleCompra
from proveedores.serializers import ProveedorSerializer
from catalogo.serializers import ProductoListSerializer


class DetalleCompraSerializer(serializers.ModelSerializer):
    producto = ProductoListSerializer(read_only=True)

    class Meta:
        model = DetalleCompra
        fields = [
            'id', 'compra', 'producto', 'unidades', 'precio',
            'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'is_active']


class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = [
            'id', 'proveedor', 'total', 'estado', 'nro_factura',
            'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'is_active']


class CompraListSerializer(CompraSerializer):
    proveedor_detalle = ProveedorSerializer(source='proveedor', read_only=True)
    detalles = DetalleCompraSerializer(many=True, read_only=True)

    class Meta(CompraSerializer.Meta):
        fields = CompraSerializer.Meta.fields + [
            'proveedor_detalle', 'detalles',
        ]
