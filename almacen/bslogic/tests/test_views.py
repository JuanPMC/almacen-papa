from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class ExampleViewTest(APITestCase):
    def test_example_endpoint(self):
        # Replace 'example' with actual endpoint
        url = reverse('example-endpoint')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
