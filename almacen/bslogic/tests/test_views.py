# bslogic/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from bslogic.models import Actuacion, Almacen, Empresa, Estado, Tipo, Inventario, ListadoActuacion, ListadoDocumentos, CaracteristicasUsuario
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied


class ApiTestCase(APITestCase):

    def setUp(self):
        # Create user:
        self.user = User.objects.create_user(
            "john", "lennon@thebeatles.com", "johnpassword")
        CaracteristicasUsuario.objects.create(
            usuario=self.user, is_editor=True)

        # Enforce Auth
        self.client.force_login(self.user)

        # Create empresas
        self.empresa = Empresa.objects.create(
            nombre='Empresa 1', ubicacion='Ubicación 1', contacto='Contacto 1')
        self.empresa.empleados.set([self.user])

        # This empresa will be used to test security
        self.otra_empresa = Empresa.objects.create(
            nombre='Empresa 2', ubicacion='Ubicación 2', contacto='Contacto 2')

        # Create sample data for testing
        self.estado = Estado.objects.create(
            estado='Activo', empresa=self.empresa)
        self.tipo = Tipo.objects.create(tipo='Tipo A', empresa=self.empresa)
        self.almacen = Almacen.objects.create(
            laboratorio='Laboratorio 1', almacen='Almacen 1', empresa=self.empresa)
        self.almacen2 = Almacen.objects.create(
            laboratorio='Laboratorio 2', almacen='Almacen 2', empresa=self.empresa)
        self.almacen_de_otra_empresa = Almacen.objects.create(
            laboratorio='Laboratorio 3', almacen='Almacen 3', empresa=self.otra_empresa)

        # Create Actuacion instance
        self.actuacion = Actuacion.objects.create(
            actuacion='Mantenimiento', empresa=self.empresa)

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
            producto=self.inventario,
            titulo="Test doc",
            documento="test_doc.txt",
            fecha='2025-01-01'
        )

    def test_get_actuaciones(self):
        # Test the GET request for Actuaciones
        response = self.client.get('/api/actuaciones/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return the one Actuacion created in setUp
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['actuacion'], 'Mantenimiento')

    def test_get_almacenes(self):
        # Test the GET request for Almacenes
        response = self.client.get('/api/almacenes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return the one Almacen created in setUp
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['almacen'], 'Almacen 1')

    def test_create_inventario(self):
        # Test the POST request to create an Inventario
        data = {
            'equipo': 'Equipo 2',
            'etiqueta': '123456',
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
        # assert that this user should not be allowed to create empresas
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_tipo(self):
        # Test the GET request for Tipo
        response = self.client.get('/api/tipos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return the one Tipo created in setUp
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tipo'], 'Tipo A')

    def test_get_estado(self):
        # Test the GET request for Estado
        response = self.client.get('/api/estados/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return the one Estado created in setUp
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['estado'], 'Activo')

    def test_get_listadoactuacion(self):
        # Test the GET request for ListadoActuacion
        response = self.client.get('/api/listadosactuacion/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return the one ListadoActuacion created in setUp
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['producto'], 1)
        self.assertEqual(response.data[0]['actuacion'], 1)

    def test_get_listadodocumento(self):
        response = self.client.get('/api/listadosdocumentos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return the one ListadoActuacion created in setUp
        self.assertEqual(len(response.data), 1)

    def test_get_inventario(self):
        # Test the GET request for Actuaciones
        response = self.client.get('/api/inventarios/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["estado"]
                         ["estado"], 'Activo', response.data)

    def test_mover_inventario(self):
        # Check a valid movement
        response = self.client.get(
            f'/api/mover-inventario?id_elemento={self.inventario.id}&id_destino={self.almacen2.id}')
        self.assertEqual(response.json(), {"status": "Ok"}, response.json())
        # Check results in the database
        self.inventario.refresh_from_db()
        self.assertEqual(self.inventario.almacen, self.almacen2)

        # Check an invalid movement
        try:
            response = self.client.get(
                '/api/mover-inventario?id_elemento=1&id_destino=5')
            self.assert_(False, "should raise an exception")
        except Exception:
            pass

        # Check un-autorized
        response = self.client.get(
            f'/api/mover-inventario?id_elemento={self.inventario.id}&id_destino={self.almacen_de_otra_empresa.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
