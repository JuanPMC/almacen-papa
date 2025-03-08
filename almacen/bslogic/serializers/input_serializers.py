from rest_framework import serializers


class MoveInventarioActionSerializer(serializers.Serializer):
    id_elemento = serializers.IntegerField(required=True)
    id_destino = serializers.IntegerField(required=True)
