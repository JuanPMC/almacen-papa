from django.db import models

class Actuacion(models.Model):
    actuacion = models.CharField(max_length=255)

    def __str__(self):
        return self.actuacion


class Almacen(models.Model):
    laboratorio = models.CharField(max_length=255)
    almacen = models.CharField(max_length=255)

    def __str__(self):
        return self.almacen


class Empresa(models.Model):
    nombre = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255)
    contacto = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Estado(models.Model):
    estado = models.CharField(max_length=255)

    def __str__(self):
        return self.estado


class Tipo(models.Model):
    tipo = models.CharField(max_length=255)

    def __str__(self):
        return self.tipo


class Inventario(models.Model):
    equipo = models.CharField(max_length=255)
    etiqueta = models.CharField(max_length=255)
    numero_serie = models.CharField(max_length=255)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    marca = models.CharField(max_length=255)
    peso = models.CharField(max_length=255)
    numero_bultos = models.IntegerField()
    coste_adecuacion = models.DecimalField(max_digits=10, decimal_places=2)
    valor_estimado = models.DecimalField(max_digits=10, decimal_places=2)
    reservado_a = models.CharField(max_length=255, blank=True, null=True)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    imagen_inicial = models.CharField(max_length=255, blank=True, null=True)
    imagen_final = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.equipo


class ListadoActuacion(models.Model):
    producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    actuacion = models.ForeignKey(Actuacion, on_delete=models.CASCADE)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.producto.equipo} - {self.actuacion.actuacion} ({self.fecha})"


class ListadoDocumentos(models.Model):
    producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    documento = models.CharField(max_length=255)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.producto.equipo} - {self.titulo} : {self.documento} ({self.fecha})"