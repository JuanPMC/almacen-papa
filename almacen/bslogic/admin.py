from django.contrib import admin
from .models import (
    Empresa,
    Actuacion,
    Almacen,
    Estado,
    Tipo,
    Inventario,
    ListadoActuacion,
    ListadoDocumentos,
    CaracteristicasUsuario
)

# Register the models in the Django admin
admin.site.register(Empresa)
admin.site.register(Actuacion)
admin.site.register(Almacen)
admin.site.register(Estado)
admin.site.register(Tipo)
admin.site.register(Inventario)
admin.site.register(ListadoActuacion)
admin.site.register(ListadoDocumentos)
admin.site.register(CaracteristicasUsuario)
