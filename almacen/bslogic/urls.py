from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ActuacionViewSet,
    AlmacenViewSet,
    EmpresaViewSet,
    EstadoViewSet,
    TipoViewSet,
    InventarioViewSet,
    ListadoActuacionViewSet,
    ListadoDocumentosViewSet,
    MoveInventario
)

router = DefaultRouter()
router.register(r'actuaciones', ActuacionViewSet)
router.register(r'almacenes', AlmacenViewSet)
router.register(r'empresas', EmpresaViewSet)
router.register(r'estados', EstadoViewSet)
router.register(r'tipos', TipoViewSet)
router.register(r'inventarios', InventarioViewSet)
router.register(r'listadosactuacion', ListadoActuacionViewSet)
router.register(r'listadosdocumentos', ListadoDocumentosViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('mover-inventario', MoveInventario.as_view(),
         name='mover-inventario')
]
