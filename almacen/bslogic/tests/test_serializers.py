from django.test import TestCase
from bslogic.serializers import ExampleSerializer

class ExampleSerializerTest(TestCase):
    def test_serializer_fields(self):
        data = {'field': 'value'}
        serializer = ExampleSerializer(data=data)
        self.assertTrue(serializer.is_valid())
