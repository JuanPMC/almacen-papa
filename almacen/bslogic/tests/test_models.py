from django.test import TestCase
from bslogic.models import ExampleModel

class ExampleModelTest(TestCase):
    def test_str_representation(self):
        example = ExampleModel.objects.create(field="value")
        self.assertEqual(str(example), "value")
