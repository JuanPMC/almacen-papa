from bslogic.models import Empresa, User, Actuacion, ListadoActuacion, Inventario, Almacen
from django.utils.timezone import now


def is_employee(usuario, empresa: Empresa) -> bool:
    return empresa.empleados.filter(id=usuario.id).exists()


def create_movement_action(almacen_id, producto_id, empresa: Empresa):
    # initialize variables
    producto = Inventario.objects.get(id=producto_id)
    alamcen_destino = Almacen.objects.get(id=almacen_id)
    almacen_inicial = producto.almacen
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
