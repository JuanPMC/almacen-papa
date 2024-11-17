from rest_framework import serializers
from bslogic.models import TipoDeProducto, TipoDeAccion, Almacen, Producto, Accion

class TipoDeProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDeProducto
        fields = ['id', 'nombre', 'descripcion']

class TipoDeAccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDeAccion
        fields = ['id', 'nombre', 'descripcion']

class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = ['id', 'nombre', 'direccion', 'creado_en']

class ProductoSerializer(serializers.ModelSerializer):
    tipo = serializers.PrimaryKeyRelatedField(queryset=TipoDeProducto.objects.all())
    almacen = serializers.PrimaryKeyRelatedField(queryset=Almacen.objects.all())
    
    class Meta:
        model = Producto
        fields = ['id', 'tipo', 'detalles', 'almacen', 'creado_en']
    
    def to_representation(self, instance):
        # Override to represent the related fields as full dict on GET requests
        representation = super().to_representation(instance)
        representation['tipo'] = TipoDeProductoSerializer(instance.tipo).data
        representation['almacen'] = AlmacenSerializer(instance.almacen).data
        return representation

class AccionSerializer(serializers.ModelSerializer):
    tipo = serializers.PrimaryKeyRelatedField(queryset=TipoDeAccion.objects.all())
    producto_almacen = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    
    class Meta:
        model = Accion
        fields = ['id', 'tipo', 'producto_almacen', 'realizado_en']
    
    def to_representation(self, instance):
        # Override to represent the related fields as full dict on GET requests
        representation = super().to_representation(instance)
        representation['tipo'] = TipoDeAccionSerializer(instance.tipo).data
        representation['producto_almacen'] = ProductoSerializer(instance.producto_almacen).data
        return representation