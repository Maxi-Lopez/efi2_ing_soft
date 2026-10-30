from rest_framework import serializers
from .models import (
    Categoria,
    Marca,
    Producto,
)

class SlugGetOrCreateField(serializers.SlugRelatedField):
    def get_queryset(self):
        return self.queryset

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            obj, _ = queryset.get_or_create(**{self.slug_field: data})
            return obj
        except (TypeError, ValueError):
            self.fail('invalid')

#MARCA
class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = [
            'id', 'nombre', 'logo', 'descripcion',
            'pais_origen', 'is_active', 'created_at',
        ]
        read_only_fields = ['id','is_active','created_at']

#CATEGORIA
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id', 'nombre', 'descripcion', 'is_active', 'created_at',
        ]
        read_only_fields = ['id', 'created_at','is_active']


#PRODUCTO
class ProductoSerializer(serializers.ModelSerializer):
    marca = SlugGetOrCreateField(
        slug_field='nombre',
        queryset=Marca.objects.all(),
        required=True
    )
    categoria = SlugGetOrCreateField(
        slug_field='nombre',
        queryset=Categoria.objects.all(),
        required=True
    )

    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion_corta', 'descripcion_larga',
            'sku', 'precio_lista', 'precio_oferta',
            'stock_total', 'is_active', 'destacado',
            'marca', 'categoria',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'is_active']

    def create(self, validated_data):
        marca = validated_data.pop('marca')
        categoria = validated_data.pop('categoria')
        
        producto = Producto.objects.create(
            marca=marca,
            categoria=categoria,
            **validated_data
        )
        return producto

    def update(self, instance, validated_data):
        marca = validated_data.pop('marca', None)
        categoria = validated_data.pop('categoria', None)
        
        if marca:
            instance.marca = marca
        
        if categoria:
            instance.categoria = categoria
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class ProductoListSerializer(ProductoSerializer):
    marca = MarcaSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    
    class Meta(ProductoSerializer.Meta):
        fields = ProductoSerializer.Meta.fields + [
            'marca', 'categoria',
        ]