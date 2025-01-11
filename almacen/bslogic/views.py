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
        return Almacen.objects.filter(empresa__empleados=user)

    def perform_update(self, serializer):
        """
        Override perform_update to enforce the permission before update
        """
        user = self.request.user
        almacen = serializer.instance
        if is_employee(user,almacen.empresa):
            return super().perform_update(serializer)
        else:
            raise PermissionDenied("You are not authorized to update this.")

    def perform_destroy(self, instance):
        """
        Override perform_destroy to enforce the permission before deletion
        """
        user = self.request.user
        almacen = instance
        if is_employee(user,almacen.empresa):
            return super().perform_destroy(instance)
        else:
            raise PermissionDenied("You are not authorized to delete this.")
        
    def perform_create(self, serializer):
        """
        Custom create method to ensure that the user belongs to the company
        that owns the Almacen.
        """
        # Get the authenticated user
        user = self.request.user
        
        # Get the empresa (company) that the user belongs to
        empresa = user.empresas.first()  # Assuming the user is linked to only one empresa
        
        # Ensure the empresa exists
        if not empresa:
            raise PermissionDenied("User is not associated with any Empresa.")
        
        # Set the empresa of the Almacen to the user's empresa
        serializer.save(empresa=empresa)

class InventarioViewSet(BaseModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer

    def get_queryset(self):
        user = self.request.user
        return Inventario.objects.filter(almacen__empresa__empleados=user)
    def perform_create(self, serializer):
        user = self.request.user
        empresa: Empresa = user.empresas.first()
        producto: Inventario = serializer.validated_data
        if producto.get("almacen").empresa != empresa or producto.get("tipo").empresa != empresa or producto.get("estado").empresa != empresa:
            raise PermissionDenied()
        return super().perform_create(serializer)
    def perform_update(self, serializer):
        user = self.request.user
        empresa: Empresa = user.empresas.first()
        producto: Inventario = serializer.instance
        if producto.get("almacen").empresa != empresa or producto.get("tipo").empresa != empresa or producto.get("estado").empresa != empresa:
            raise PermissionDenied()
        return super().perform_update(serializer)    

class ListadoActuacionViewSet(BaseModelViewSet):
    queryset = ListadoActuacion.objects.all()
    serializer_class = ListadoActuacionSerializer

    def get_queryset(self):
        user = self.request.user
        return ListadoActuacion.objects.filter(producto__almacen__empresa__empleados=user)
    def perform_create(self, serializer):
        user = self.request.user
        empresa: Empresa = user.empresas.first()
        actuacion: ListadoActuacion = serializer.instance
        if actuacion.producto.almacen.empresa != empresa:
            raise PermissionDenied()
        return super().perform_create(serializer)
    def perform_update(self, serializer):
        user = self.request.user
        empresa: Empresa = user.empresas.first()
        actuacion: ListadoActuacion = serializer.instance
        if actuacion.producto.almacen.empresa != empresa:
            raise PermissionDenied()
        return super().perform_update(serializer)    


class ListadoDocumentosViewSet(BaseModelViewSet):
    queryset = ListadoDocumentos.objects.all()
    serializer_class = ListadoDocumentosSerializer

    def get_queryset(self):
        user = self.request.user
        return ListadoDocumentos.objects.filter(producto__almacen__empresa__empleados=user)
    def perform_create(self, serializer):
        user = self.request.user
        empresa: Empresa = user.empresas.first()
        documento: ListadoDocumentos = serializer.instance
        if documento.producto.almacen.empresa != empresa:
            raise PermissionDenied("Dont have permission to perform this operation")
        return super().perform_create(serializer)
    def perform_update(self, serializer):
        user = self.request.user
        empresa: Empresa = user.empresas.first()
        documento: ListadoDocumentos = serializer.instance
        if documento.producto.almacen.empresa != empresa:
            raise PermissionDenied("Dont have permission to perform this operation")
        return super().perform_update(serializer)    
    
class EmpresaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class EstadoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class TipoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer