from rest_framework.test import APITestCase
from rest_framework import status
from bslogic.models import TipoDeProducto, Almacen, Producto

class ProductoViewSetTest(APITestCase):
    def setUp(self):
        self.tipo_producto = TipoDeProducto.objects.create(nombre="Electrónica", descripcion="Productos electrónicos")
        self.almacen = Almacen.objects.create(nombre="Almacen Central", direccion="Calle Falsa 123")

    def test_create_producto(self):
        # Create a new producto with only IDs for related fields
        data = {
            'tipo': self.tipo_producto.id,
            'detalles': 'Detalles del producto',
            'almacen': self.almacen.id
        }
        response = self.client.post('/api/productos/', data, format="json", headers={"Accept":"application/json"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response)
        self.assertEqual(response.data['tipo']['id'], self.tipo_producto.id)
        self.assertEqual(response.data['almacen']['id'], self.almacen.id)

    def test_get_producto(self):
        # Retrieve the producto and check that the related fields are serialized fully
        producto = Producto.objects.create(tipo=self.tipo_producto, almacen=self.almacen, detalles='Detalles del producto')
        response = self.client.get(f'/api/productos/{producto.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tipo']['id'], self.tipo_producto.id)
        self.assertEqual(response.data['almacen']['id'], self.almacen.id)
        self.assertEqual(response.data['tipo']['nombre'], self.tipo_producto.nombre)
        self.assertEqual(response.data['almacen']['nombre'], self.almacen.nombre)
