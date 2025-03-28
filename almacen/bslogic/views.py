from rest_framework import viewsets
from bslogic.models import Actuacion, Almacen, Empresa, Estado, Tipo, Inventario, ListadoActuacion, ListadoDocumentos
from bslogic.serializers.model_serializers import ActuacionSerializer, AlmacenSerializer, EmpresaSerializer, EstadoSerializer, TipoSerializer, InventarioSerializer, ListadoActuacionSerializer, ListadoDocumentosSerializer
from bslogic.serializers.input_serializers import MoveInventarioActionSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from bslogic.permissions import AlmacenPermission
from bslogic.operations import is_employee, create_movement_action
from rest_framework.exceptions import PermissionDenied
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAdminUser


class BaseView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AlmacenPermission]


class BaseModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AlmacenPermission]


class ActuacionViewSet(BaseModelViewSet):
    queryset = Actuacion.objects.all()
    serializer_class = ActuacionSerializer

    def get_queryset(self):
        user = self.request.user
        return Actuacion.objects.filter(empresa__empleados=user)

    def perform_update(self, serializer):
        """
        Override perform_update to enforce the permission before update
        """
        user = self.request.user
        actuacion = serializer.instance
        if is_employee(user, actuacion.empresa):
            return super().perform_update(serializer)
        else:
            raise PermissionDenied("You are not authorized to update this.")

    def perform_destroy(self, instance):
        """
        Override perform_destroy to enforce the permission before deletion
        """
        user = self.request.user
        actuacion = instance
        if is_employee(user, actuacion.empresa):
            return super().perform_destroy(instance)
        else:
            raise PermissionDenied("You are not authorized to delete this.")

    def perform_create(self, serializer):
        """
        Custom create method to ensure that the user belongs to the company
        that owns the actuacion.
        """
        # Get the authenticated user
        user = self.request.user

        # Get the empresa (company) that the user belongs to
        empresa = user.empresas.first()  # Assuming the user is linked to only one empresa

        # Ensure the empresa exists
        if not empresa:
            raise PermissionDenied("User is not associated with any Empresa.")

        # Set the empresa of the actuacion to the user's empresa
        serializer.save(empresa=empresa)


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
        if is_employee(user, almacen.empresa):
            return super().perform_update(serializer)
        else:
            raise PermissionDenied("You are not authorized to update this.")

    def perform_destroy(self, instance):
        """
        Override perform_destroy to enforce the permission before deletion
        """
        user = self.request.user
        almacen = instance
        if is_employee(user, almacen.empresa):
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
        if producto.almacen.empresa != empresa or producto.tipo.empresa != empresa or producto.estado.empresa != empresa:
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
        actuacion: ListadoActuacion = serializer.validated_data
        if actuacion.get("producto").almacen.empresa != empresa:
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
        documento: ListadoDocumentos = serializer.validated_data
        if documento.get("producto").almacen.empresa != empresa:
            raise PermissionDenied(
                "Dont have permission to perform this operation")
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        user = self.request.user
        empresa: Empresa = user.empresas.first()
        documento: ListadoDocumentos = serializer.instance
        if documento.producto.almacen.empresa != empresa:
            raise PermissionDenied(
                "Dont have permission to perform this operation")
        return super().perform_update(serializer)

    @action(detail=True, methods=['get'], permission_classes=[AlmacenPermission])
    def download(self, request, pk=None):
        """Serve the file securely."""
        documento = get_object_or_404(ListadoDocumentos, pk=pk)

        # Ensure the user has access
        user = self.request.user
        if documento.producto.almacen.empresa not in user.empresas.all():
            return Response({'error': 'Unauthorized'}, status=403)

        file_path = documento.datos_del_documento.path
        if not os.path.exists(file_path):
            return Response({'error': 'File not found'}, status=404)

        return FileResponse(open(file_path, 'rb'))


class EmpresaViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


class EstadoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer


class TipoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer


class MoveInventario(BaseView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="id_elemento", description="Identificador del inventario(producto)", required=True, type=str),
            OpenApiParameter(
                name="id_destino", description="Identificador del destino", required=True, type=str)
        ]
    )
    def get(self, request):
        # Get the user info
        user = self.request.user
        empresa: Empresa = user.empresas.first()
        # Validate input data
        serializer = MoveInventarioActionSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        # Get the input data
        id_elemento = serializer.validated_data["id_elemento"]
        id_destino = serializer.validated_data["id_destino"]

        if not create_movement_action(id_destino, id_elemento, empresa):
            return Response({"status": "Error"}, status=500)
        return Response({"status": "Ok"})


class GetUserInfo(BaseView):
    def get(self, request) -> bool:
        is_editor = request.user and request.user.caracteristicas and request.user.caracteristicas.is_editor
        return Response({"is_editor": is_editor})
