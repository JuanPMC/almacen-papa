from bslogic.models import Empresa, User, Actuacion, ListadoActuacion, Inventario, Almacen
from django.utils.timezone import now
from rest_framework.exceptions import PermissionDenied


def is_employee(usuario, empresa: Empresa) -> bool:
    return empresa.empleados.filter(id=usuario.id).exists()


def check_movement_permissions(producto: Inventario, empresa_usuario: Empresa, almacen1: Almacen, almacen2: Almacen):
    almacen1_es_misma_empresa = almacen1.empresa == empresa_usuario
    almacen2_es_misma_empresa = almacen2.empresa == empresa_usuario
    producto_es_de_empresa = producto.almacen.empresa == empresa_usuario

    return (almacen1_es_misma_empresa and almacen2_es_misma_empresa and producto_es_de_empresa)


def create_movement_action(almacen_id, producto_id, empresa: Empresa):
    # initialize variables
    producto = Inventario.objects.get(id=producto_id)
    alamcen_destino = Almacen.objects.get(id=almacen_id)
    almacen_inicial = producto.almacen

    if not check_movement_permissions(producto, empresa, almacen_inicial, alamcen_destino):
        raise PermissionDenied()

    description = f"Movido el producto: {producto} de {almacen_inicial} a {alamcen_destino}"

    # modify  product
    producto.almacen = alamcen_destino
    producto.save()

    # Get or create Actuacion
    actuacion, _ = Actuacion.objects.get_or_create(
        empresa=empresa,
        actuacion="Movimiento"
    )
    # Creatre listadeactuaciones
    nueva_lista_actuaciones = ListadoActuacion.objects.create(
        producto=producto, actuacion=actuacion, fecha=now(), descripcion=description)

    return (nueva_lista_actuaciones is not None)
