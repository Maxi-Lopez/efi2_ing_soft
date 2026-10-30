from rest_framework import serializers
from django.contrib.auth.models import Group
from .models import UsuarioPersonalizado, ListaDeseosProductos
from catalogo.serializers import ProductoListSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Si es superusuario, siempre es admin
        if user.is_superuser:
            token['role'] = 'admin'
        else:
            # Si no, buscamos en los grupos y forzamos minúsculas
            groups = user.groups.all()
            token['role'] = groups.first().name.lower() if groups else ''

        return token

#Serializer GET usuario
class UsuarioPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioPersonalizado
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'telefono',
            'dni',
            'email',
            'groups'
        ]

#Serializer POST usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioPersonalizado
        fields = [
            'id',
            'username',
            'last_name',
            'first_name',
            'password',
            'telefono',
            'email',
            'dni',
        ]
        read_only_fields=['id']
        #Indica que el campo 'password' es de solo escritura
        extra_kwargs = {
            'password': {'write_only': True}
            }
    def create(self, validated_data):
            return UsuarioPersonalizado.objects.create_user(**validated_data)        


class ListaDeseosPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaDeseosProductos
        fields=[
            'producto'
        ]
        read_only_fields = ['id', 'fecha_at', 'is_active','usuario',]

class ListaDeseosGetSerializer(serializers.ModelSerializer):
    usuario = UsuarioPublicSerializer(read_only=True)
    producto = ProductoListSerializer(read_only=True)

    class Meta:
        model = ListaDeseosProductos
        fields=[
            'id',
            'usuario',
            'producto'
        ]

