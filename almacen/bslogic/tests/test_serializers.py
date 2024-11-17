from django.test import TestCase
from rest_framework.exceptions import ValidationError
from bslogic.models import TipoDeProducto, TipoDeAccion, Almacen, Producto, Accion
from bslogic.serializers.model_serializers import TipoDeProductoSerializer, TipoDeAccionSerializer, AlmacenSerializer, ProductoSerializer, AccionSerializer

class TipoDeProductoSerializerTest(TestCase):
    def test_valid_data(self):
        data = {'nombre': 'Electrónica', 'descripcion': 'Productos electrónicos'}
        serializer = TipoDeProductoSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['nombre'], 'Electrónica')
        self.assertEqual(serializer.validated_data['descripcion'], 'Productos electrónicos')

    def test_invalid_data(self):
        data = {'nombre': 'Electrónica', 'descripcion':False}
        serializer = TipoDeProductoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('descripcion', serializer.errors)

class TipoDeAccionSerializerTest(TestCase):
    def test_valid_data(self):
        data = {'nombre': 'Venta', 'descripcion': 'Venta de productos'}
        serializer = TipoDeAccionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['nombre'], 'Venta')
        self.assertEqual(serializer.validated_data['descripcion'], 'Venta de productos')

    def test_invalid_data(self):
        data = {'nombre': 'Venta', 'descripcion':False}
        serializer = TipoDeAccionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('descripcion', serializer.errors)

class AlmacenSerializerTest(TestCase):
    def test_valid_data(self):
        almacen = Almacen.objects.create(nombre="Almacen Central", direccion="Calle Falsa 123")
        serializer = AlmacenSerializer(almacen)
        self.assertEqual(serializer.data['nombre'], 'Almacen Central')
        self.assertEqual(serializer.data['direccion'], 'Calle Falsa 123')

class ProductoSerializerTest(TestCase):
    def setUp(self):
        self.tipo_producto = TipoDeProducto.objects.create(nombre="Electrónica", descripcion="Productos electrónicos")
        self.almacen = Almacen.objects.create(nombre="Almacen Central", direccion="Calle Falsa 123")

    def test_valid_data(self):
        data = {
            'tipo': self.tipo_producto.id,
            'detalles': 'Detalles del producto',
            'almacen': self.almacen.id
        }
        serializer = ProductoSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['tipo'], self.tipo_producto)
        self.assertEqual(serializer.validated_data['almacen'], self.almacen)

    def test_invalid_data(self):
        data = {'tipo': None, 'detalles': 'Detalles sin tipo', 'almacen': None}
        serializer = ProductoSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('tipo', serializer.errors)
        self.assertIn('almacen', serializer.errors)

class AccionSerializerTest(TestCase):
    def setUp(self):
        self.tipo_producto = TipoDeProducto.objects.create(nombre="Electrónica", descripcion="Productos electrónicos")
        self.tipo_accion = TipoDeAccion.objects.create(nombre="Venta", descripcion="Venta de productos")
        self.almacen = Almacen.objects.create(nombre="Almacen Central", direccion="Calle Falsa 123")
        self.producto = Producto.objects.create(tipo=self.tipo_producto, almacen=self.almacen, detalles="Detalles del producto")

    def test_valid_data(self):
        data = {
            'tipo': self.tipo_accion.id,
            'producto_almacen': self.producto.id
        }
        serializer = AccionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['tipo'], self.tipo_accion)
        self.assertEqual(serializer.validated_data['producto_almacen'], self.producto)

    def test_invalid_data(self):
        data = {'tipo': None, 'producto_almacen': None}
        serializer = AccionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('tipo', serializer.errors)
        self.assertIn('producto_almacen', serializer.errors)
