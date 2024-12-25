from rest_framework import viewsets
from bslogic.models import Actuacion, Almacen, Empresa, Estado, Tipo, Inventario, ListadoActuacion
from bslogic.serializers.model_serializers import ActuacionSerializer, AlmacenSerializer, EmpresaSerializer, EstadoSerializer, TipoSerializer, InventarioSerializer, ListadoActuacionSerializer

class ActuacionViewSet(viewsets.ModelViewSet):
    queryset = Actuacion.objects.all()
    serializer_class = ActuacionSerializer

class AlmacenViewSet(viewsets.ModelViewSet):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class TipoViewSet(viewsets.ModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer

class ListadoActuacionViewSet(viewsets.ModelViewSet):
    queryset = ListadoActuacion.objects.all()
    serializer_class = ListadoActuacionSerializer