from rest_framework import viewsets
from bslogic.models import Actuacion, Almacen, Empresa, Estado, Tipo, Inventario, ListadoActuacion, ListadoDocumentos
from bslogic.serializers.model_serializers import ActuacionSerializer, AlmacenSerializer, EmpresaSerializer, EstadoSerializer, TipoSerializer, InventarioSerializer, ListadoActuacionSerializer, ListadoDocumentosSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from bslogic.operations import is_employee
from rest_framework.exceptions import PermissionDenied


class BaseModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class ActuacionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Actuacion.objects.all()
    serializer_class = ActuacionSerializer
    

class AlmacenViewSet(BaseModelViewSet):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer

    def get_queryset(self):
        """
        Override to filter Inventario based on the user's company
        """
        user = self.request.user.id
        # Retrieve all Inventario related to the user's empresa
        return Inventario.objects.filter(almacen__empresa__empleados=user)

    def perform_update(self, serializer):
        """
        Override perform_update to enforce the permission before update
        """
        user = self.request.user
        almacen = serializer.instance.almacen
        if is_employee(user,almacen.empresa):
            return super().perform_update(serializer)
        else:
            raise PermissionDenied("You are not authorized to update this Inventario.")

    def perform_destroy(self, instance):
        """
        Override perform_destroy to enforce the permission before deletion
        """
        user = self.request.user
        almacen = instance.almacen
        if is_employee(user,almacen.empresa):
            return super().perform_destroy(instance)
        else:
            raise PermissionDenied("You are not authorized to delete this Inventario.")


class EmpresaViewSet(BaseModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class EstadoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class TipoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer

class InventarioViewSet(BaseModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer

class ListadoActuacionViewSet(BaseModelViewSet):
    queryset = ListadoActuacion.objects.all()
    serializer_class = ListadoActuacionSerializer

class ListadoDocumentosViewSet(BaseModelViewSet):
    queryset = ListadoDocumentos.objects.all()
    serializer_class = ListadoDocumentosSerializer