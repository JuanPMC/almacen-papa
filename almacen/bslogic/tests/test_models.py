from django.test import TestCase
from bslogic.models import TipoDeProducto, TipoDeAccion, Almacen, Producto, Accion

class TipoDeProductoModelTest(TestCase):
    def test_tipo_de_producto_creation(self):
        tipo = TipoDeProducto.objects.create(nombre="Electrónica", descripcion="Productos electrónicos")
        self.assertEqual(tipo.nombre, "Electrónica")
        self.assertEqual(tipo.descripcion, "Productos electrónicos")
        self.assertEqual(str(tipo), "Electrónica")

class TipoDeAccionModelTest(TestCase):
    def test_tipo_de_accion_creation(self):
        tipo = TipoDeAccion.objects.create(nombre="Venta", descripcion="Venta de productos")
        self.assertEqual(tipo.nombre, "Venta")
        self.assertEqual(tipo.descripcion, "Venta de productos")
        self.assertEqual(str(tipo), "Venta")

class AlmacenModelTest(TestCase):
    def test_almacen_creation(self):
        almacen = Almacen.objects.create(nombre="Almacen Central", direccion="Calle Falsa 123")
        self.assertEqual(almacen.nombre, "Almacen Central")
        self.assertEqual(almacen.direccion, "Calle Falsa 123")
        self.assertTrue(almacen.creado_en)  # Ensure created_at is set
        self.assertEqual(str(almacen), "Almacen Central")

class ProductoModelTest(TestCase):
    def setUp(self):
        self.tipo = TipoDeProducto.objects.create(nombre="Electrónica", descripcion="Productos electrónicos")
        self.almacen = Almacen.objects.create(nombre="Almacen Central", direccion="Calle Falsa 123")

    def test_producto_creation(self):
        producto = Producto.objects.create(tipo=self.tipo, almacen=self.almacen, detalles="Detalles del producto")
        self.assertEqual(producto.tipo, self.tipo)
        self.assertEqual(producto.almacen, self.almacen)
        self.assertEqual(producto.detalles, "Detalles del producto")
        self.assertTrue(producto.creado_en)  # Ensure created_at is set
        self.assertEqual(str(producto), f"{self.tipo.nombre} - {producto.id}")

class AccionModelTest(TestCase):
    def setUp(self):
        self.tipo_producto = TipoDeProducto.objects.create(nombre="Electrónica", descripcion="Productos electrónicos")
        self.tipo_accion = TipoDeAccion.objects.create(nombre="Venta", descripcion="Venta de productos")
        self.almacen = Almacen.objects.create(nombre="Almacen Central", direccion="Calle Falsa 123")
        self.producto = Producto.objects.create(tipo=self.tipo_producto, almacen=self.almacen, detalles="Detalles del producto")

    def test_accion_creation(self):
        accion = Accion.objects.create(tipo=self.tipo_accion, producto_almacen=self.producto)
        self.assertEqual(accion.tipo, self.tipo_accion)
        self.assertEqual(accion.producto_almacen, self.producto)
        self.assertTrue(accion.realizado_en)  # Ensure realizado_en is set
        self.assertEqual(str(accion), f"{self.tipo_accion.nombre}: sobre {self.producto.tipo.nombre} en {self.producto.almacen.nombre}")
