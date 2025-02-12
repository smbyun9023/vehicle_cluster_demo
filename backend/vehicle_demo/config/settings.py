#config/settings.py
import os
from pathlib import Path

# 기본 설정
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

# 데이터베이스 설정
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "vehicle_demo"),
        "USER": os.getenv("POSTGRES_USER", "debug"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "debug"),
        "HOST": os.getenv("POSTGRES_HOST", "postgres"),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
    },
    "mongo": {
        "ENGINE": "djongo",
        "NAME": "vehicle_demo_mongo",
        "CLIENT": {
            "host": "mongodb://root:rootpassword@mongodb:27017/",
        }
    }
}

# Swagger 설정
INSTALLED_APPS = [
    # 기타 앱들...
    'rest_framework',
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'vehicle_demo API',
    'DESCRIPTION': 'API Documentation for vehicle_demo',
    'VERSION': '1.0.0',
    'SERVE_PERMISSIONS': ['rest_framework.permissions.IsAdminUser'],
}

# Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 기타 설정들...
