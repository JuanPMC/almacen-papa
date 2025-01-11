# bslogic/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from bslogic.models import Actuacion, Almacen, Empresa, Estado, Tipo, Inventario, ListadoActuacion, ListadoDocumentos
from django.contrib.auth.models import User

class ApiTestCase(APITestCase):

    def setUp(self):
        # Create user:
        self.user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
        # Enforce Auth
        self.client.force_login(self.user)

        # Create empresa
        self.empresa = Empresa.objects.create(nombre='Empresa 1', ubicacion='Ubicación 1', contacto='Contacto 1')
        self.empresa.empleados.set([self.user])

        # Create sample data for testing
        self.estado = Estado.objects.create(estado='Activo', empresa=self.empresa)
        self.tipo = Tipo.objects.create(tipo='Tipo A', empresa=self.empresa)
        self.almacen = Almacen.objects.create(laboratorio='Laboratorio 1', almacen='Almacen 1', empresa=self.empresa)

        # Create Actuacion instance
        self.actuacion = Actuacion.objects.create(actuacion='Mantenimiento', empresa=self.empresa)

        # Create Inventario instance
        self.inventario = Inventario.objects.create(
            equipo='Equipo 1',
            numero_serie='12345',
            tipo=self.tipo,
            estado=self.estado,
            marca='Marca 1',
            peso='10kg',
            numero_bultos=5,
            coste_adecuacion=Decimal('100.00'),
            valor_estimado=Decimal('500.00'),
            reservado_a='Reservado 1',
            almacen=self.almacen,
            imagen_inicial='initial_image.jpg',
            imagen_final='final_image.jpg'
        )

        # Create ListadoActuacion instance
        self.listado_actuacion = ListadoActuacion.objects.create(
            producto=self.inventario,
            actuacion=self.actuacion,
            fecha='2024-12-25'
        )

        # Creando documento
        self.listado_documentos = ListadoDocumentos.objects.create(
            producto = self.inventario,
            titulo = "Test doc",
            documento = "test_doc.txt",
            fecha = '2025-01-01'
        )

    def test_get_actuaciones(self):
        # Test the GET request for Actuaciones
        response = self.client.get('/api/actuaciones/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return the one Actuacion created in setUp
        self.assertEqual(response.data[0]['actuacion'], 'Mantenimiento')

    def test_get_almacenes(self):
        # Test the GET request for Almacenes
        response = self.client.get('/api/almacenes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return the one Almacen created in setUp
        self.assertEqual(response.data[0]['almacen'], 'Almacen 1')

    def test_create_inventario(self):
        # Test the POST request to create an Inventario
        data = {
            'equipo': 'Equipo 2',
            'etiqueta':'123456',
            'numero_serie': '67890',
            'tipo': self.tipo.id,
            'estado': self.estado.id,
            'marca': 'Marca 2',
            'peso': '15kg',
            'numero_bultos': 10,
            'coste_adecuacion': '150.00',
            'valor_estimado': '600.00',
            'reservado_a': 'Reservado 2',
            'almacen': self.almacen.id,
            'imagen_inicial': 'new_initial_image.jpg',
            'imagen_final': 'new_final_image.jpg'
        }
        response = self.client.post('/api/inventarios/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['equipo'], 'Equipo 2')

    def test_get_empresa(self):
        # Test the GET request for Empresa
        response = self.client.get('/api/empresas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return the one Empresa created in setUp
        self.assertEqual(response.data[0]['nombre'], 'Empresa 1')

    def test_get_tipo(self):
        # Test the GET request for Tipo
        response = self.client.get('/api/tipos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return the one Tipo created in setUp
        self.assertEqual(response.data[0]['tipo'], 'Tipo A')

    def test_get_estado(self):
        # Test the GET request for Estado
        response = self.client.get('/api/estados/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return the one Estado created in setUp
        self.assertEqual(response.data[0]['estado'], 'Activo')

    def test_get_listadoactuacion(self):
        # Test the GET request for ListadoActuacion
        response = self.client.get('/api/listadosactuacion/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return the one ListadoActuacion created in setUp
        self.assertEqual(response.data[0]['producto'], 1)
        self.assertEqual(response.data[0]['actuacion'], 1)

    def test_get_listadodocumento(self):
        response = self.client.get('/api/listadosdocumentos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return the one ListadoActuacion created in setUp

