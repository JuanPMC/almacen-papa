#!/bin/bash

# Check if a project name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <project_name>"
  exit 1
fi

PROJECT_NAME=$1
APP_NAME="bslogic"
VENV_NAME="venv"

# Step 1: Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv $VENV_NAME
source $VENV_NAME/bin/activate

# Step 2: Install Django and dependencies
echo "Installing Django and dependencies..."
pip install --upgrade pip
pip install django djangorestframework drf-spectacular pytest pytest-django coverage
pip freeze > requirements.txt

# Step 3: Create Django project and app
echo "Creating Django project '$PROJECT_NAME' and app '$APP_NAME'..."
django-admin startproject $PROJECT_NAME
cd $PROJECT_NAME
python manage.py startapp $APP_NAME

# Step 4: Update settings.py
echo "Configuring settings.py..."
SETTINGS_FILE="$PROJECT_NAME/settings.py"

# Add installed apps
sed -i "/INSTALLED_APPS = \[/ a\    'rest_framework',\n    'drf_spectacular',\n    '$APP_NAME'," $SETTINGS_FILE

# Add DRF and drf-spectacular settings
cat <<EOT >> $SETTINGS_FILE

# Django Rest Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# drf-spectacular configuration
SPECTACULAR_SETTINGS = {
    'TITLE': 'My API Documentation',
    'DESCRIPTION': 'API documentation for $APP_NAME app.',
    'VERSION': '1.0.0',
}
EOT

# Step 5: Create scaffolding for tests
echo "Setting up test scaffolding..."

# Create tests folder and init file
mkdir -p $APP_NAME/tests
touch $APP_NAME/tests/__init__.py

# Create test cases for views
cat <<EOT > $APP_NAME/tests/test_views.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class ExampleViewTest(APITestCase):
    def test_example_endpoint(self):
        # Replace 'example' with actual endpoint
        url = reverse('example-endpoint')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
EOT

# Create test cases for serializers
cat <<EOT > $APP_NAME/tests/test_serializers.py
from django.test import TestCase
from $APP_NAME.serializers import ExampleSerializer

class ExampleSerializerTest(TestCase):
    def test_serializer_fields(self):
        data = {'field': 'value'}
        serializer = ExampleSerializer(data=data)
        self.assertTrue(serializer.is_valid())
EOT

# Create test cases for models
cat <<EOT > $APP_NAME/tests/test_models.py
from django.test import TestCase
from $APP_NAME.models import ExampleModel

class ExampleModelTest(TestCase):
    def test_str_representation(self):
        example = ExampleModel.objects.create(field="value")
        self.assertEqual(str(example), "value")
EOT

# Step 6: Create URLs for the app
echo "Creating URLs for $APP_NAME..."
cat <<EOT > $APP_NAME/urls.py
from django.urls import path

# Placeholder for your app's views
urlpatterns = []
EOT

# Step 7: Configure project URLs
echo "Configuring project URLs..."
cat <<EOT > $PROJECT_NAME/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('$APP_NAME.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
EOT

# Step 8: Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Step 9: Initialize pytest configuration
echo "Creating pytest configuration..."
cat <<EOT > pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = $PROJECT_NAME.settings
python_files = tests.py test_*.py *_tests.py
EOT