from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, TipoDeProductoViewSet, TipoDeAccionViewSet, AlmacenViewSet, AccionViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'tipos-producto', TipoDeProductoViewSet)
router.register(r'tipos-accion', TipoDeAccionViewSet)
router.register(r'almacenes', AlmacenViewSet)
router.register(r'acciones', AccionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
