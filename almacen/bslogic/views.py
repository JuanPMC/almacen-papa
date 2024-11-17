from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from bslogic.models import Producto, TipoDeProducto, TipoDeAccion, Almacen, Accion
from bslogic.serializers.model_serializers import ProductoSerializer, TipoDeProductoSerializer, TipoDeAccionSerializer, AlmacenSerializer, AccionSerializer

class TipoDeProductoViewSet(viewsets.ModelViewSet):
    queryset = TipoDeProducto.objects.all()
    serializer_class = TipoDeProductoSerializer

class TipoDeAccionViewSet(viewsets.ModelViewSet):
    queryset = TipoDeAccion.objects.all()
    serializer_class = TipoDeAccionSerializer

class AlmacenViewSet(viewsets.ModelViewSet):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def create(self, request, *args, **kwargs):
        # Custom create method for handling only the ID of related fields
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        # Custom list method for returning the full dict of related fields
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # Custom retrieve method for returning the full dict of related fields
        return super().retrieve(request, *args, **kwargs)

class AccionViewSet(viewsets.ModelViewSet):
    queryset = Accion.objects.all()
    serializer_class = AccionSerializer

    def create(self, request, *args, **kwargs):
        # Custom create method for handling only the ID of related fields
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        # Custom list method for returning the full dict of related fields
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # Custom retrieve method for returning the full dict of related fields
        return super().retrieve(request, *args, **kwargs)
