import os

import environ

root = environ.Path(__file__) - 2  # three folder back (/a/b/c/ - 3 = /)
BASE_DIR = root()
env = environ.Env()
env.read_env(str(root.path('.env')))


SECRET_KEY = env('DJANGO_SECRET_KEY', default='dev')

DEBUG = False

SITE_DOMAIN = env('DJANGO_SITE_DOMAIN', default='*')
SITE_PROTOCOL = env('DJANGO_SITE_PROTOCOL', default='http://')
SITE_URL = '{0}{1}'.format(SITE_PROTOCOL, SITE_DOMAIN)

ALLOWED_HOSTS = [SITE_DOMAIN]

ADMINS = [
    ('Toni Colom', 'tcolomquetglas@gmail.com')
]
ADMIN_URL = env('DJANGO_ADMIN_URL', default='admin')

# Application definition
INSTALLED_APPS = [
    # Local
    'main',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'django_extensions',
    'adminsortable2',
    # 'merged_inlines',
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

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.settings_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DJANGO_DATABASE_DEFAULT_NAME', default='acampabasquet'),
        'USER': env('DJANGO_DATABASE_DEFAULT_USER', default='acampabasquet'),
        'PASSWORD': env('DJANGO_DATABASE_DEFAULT_PASSWORD', default='acampabasquet'),
        'HOST': env('DJANGO_DATABASE_DEFAULT_HOST', default='127.0.0.1'),
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
LANGUAGE_CODE = 'ca'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Django debug toolbar settings
DEBUG_TOOLBAR = False

# Loggin
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': env('DJANGO_LOG_FILE', default='/tmp/acampabasquet.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('DJANGO_EMAIL_HOST', default='')
EMAIL_PORT = env('DJANGO_EMAIL_PORT', default='')
EMAIL_HOST_USER = env('DJANGO_EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('DJANGO_EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = True
SERVER_EMAIL = 'no-reply@3x324h.cat'

# Constants
SITE_NAME = "Acampabàsquet"

# Config
AVAILABLE_FIELDS = 2  # Matches at the same time
START_DATETIME = "2022-07-01 19:00"
MATCH_LENGTH = 20  # In minutes
