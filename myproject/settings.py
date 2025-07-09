import os
import base64
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get the Base64 encoded secret key from the environment variable.
# This variable is set by Jenkins and decoded here.
encoded_secret_key = os.environ.get('DJANGO_SECRET_KEY_B64')

if not encoded_secret_key:
    # This block will execute if DJANGO_SECRET_KEY_B64 is not set.
    # For local development without Jenkins, you might set a default here,
    # but for production, it's safer to raise an error.
    # The 'insecure-fallback-key' is for local testing only.
    print("WARNING: DJANGO_SECRET_KEY_B64 environment variable not set. Using a default insecure key.")
    SECRET_KEY = 'insecure-fallback-key-for-development-only-do-not-use-in-production'
else:
    try:
        # Decode the Base64 string to bytes, then decode bytes to UTF-8 string.
        # This is the secure way to handle special characters in the secret key.
        SECRET_KEY = base64.b64decode(encoded_secret_key).decode('utf-8')
    except (base64.binascii.Error, UnicodeDecodeError) as e:
        # Handle cases where the Base64 string is malformed or decoding fails.
        raise ImproperlyConfigured(f"Error decoding DJANGO_SECRET_KEY_B64: {e}. Ensure it's a valid Base64 string.")

# SECURITY WARNING: don't run with debug turned on in production!
# Reads DJANGO_DEBUG from environment, defaults to True for development
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# ALLOWED_HOSTS for your Django application
# Reads DJANGO_ALLOWED_HOSTS from environment, splits by comma
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Add your custom Django apps here, e.g., 'myapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database configuration
# Reads database credentials from environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'), # 'db' is the service name in docker-compose.yml
        'PORT': os.environ.get('DB_PORT'), # Default PostgreSQL port
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Directory where static files will be collected

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
