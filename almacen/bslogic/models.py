from django.db import models

class TipoDeProducto(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class TipoDeAccion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Almacen(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    tipo = models.ForeignKey(TipoDeProducto, on_delete=models.CASCADE, related_name='productos')
    detalles = models.TextField(blank=True)  # Detalles específicos del producto
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, related_name='producto_almacenes')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo.nombre} - {self.id}"  # Identificar productos individuale

class Accion(models.Model):
    tipo = models.ForeignKey(TipoDeAccion, on_delete=models.CASCADE, related_name='acciones')
    producto_almacen = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='acciones')
    realizado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.tipo.nombre}: sobre "
                f"{self.producto_almacen.tipo.nombre} en {self.producto_almacen.almacen.nombre}")
