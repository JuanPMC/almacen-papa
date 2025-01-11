from rest_framework import serializers
from bslogic.models import Actuacion, Almacen, Empresa, Estado, Tipo, Inventario, ListadoActuacion, ListadoDocumentos

class ActuacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actuacion
        fields = '__all__'

class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = '__all__'
    empresa = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all(), required=False)


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'

class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo
        fields = '__all__'

class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = '__all__'

class ListadoActuacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListadoActuacion
        fields = '__all__'

class ListadoDocumentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListadoDocumentos
        fields = '__all__'