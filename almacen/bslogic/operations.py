from bslogic.models import Empresa, User

def is_employee(usuario, empresa: Empresa) -> bool:
    return empresa.empleados.filter(id=usuario.id).exists()