import os
from pathlib import Path



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

CSRF_FAILURE_VIEW = 'portals.views.csrf_failure'
SECRET_KEY ='0pfvm$!)oc&umw95ep#gwq*as#c!*d6hhb0l8+teyxsolqn_pg'
DEBUG =True 
ALLOWED_HOSTS =['127.0.0.1','localhost','www.soinvet.com','soinvet.com','https://soinvet.com/'] 
# Application definition

INSTALLED_APPS = [
    # My apps
    'vet.apps.VetConfig',
    'user.apps.UserConfig',
    'portals.apps.PortalsConfig',
    'rest_framework',
    # Third party packages
    'crispy_forms',
    'crispy_bootstrap4',

    # Django defaults
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    
]



AUTH_USER_MODEL = 'user.User'
CRISPY_TEMPLATE_PACK = 'bootstrap4'



MIDDLEWARE = [
   'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'soin.urls'

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
                'portals.context_processor.all_farmers',
                'portals.context_processor.all_officials',
                'portals.context_processor.all_vets',
                'portals.context_processor.choices',
                'portals.context_processor.user_role',
                
            ],
        },
    },
]

WSGI_APPLICATION = 'soin.wsgi.application'
if DEBUG:
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',  # Enable browsable API only in development
        ),
        'DEFAULT_PARSER_CLASSES': (
            'rest_framework.parsers.MultiPartParser',
            'rest_framework.parsers.FormParser',
            'rest_framework.parsers.JSONParser',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'portals.permissions.Is_Vet',
            'portals.permissions.Is_Farmer',
            'portals.permissions.Is_Official',
            'portals.permissions.IsVetOrOfficial',
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10,
    }
else:
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',  
        ),
        'DEFAULT_PARSER_CLASSES': (
            'rest_framework.parsers.MultiPartParser',
            'rest_framework.parsers.FormParser',
            'rest_framework.parsers.JSONParser',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'portals.permissions.Is_Vet',
            'portals.permissions.Is_Farmer',
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 2,
    }

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        
    }
}

# DATABASES = {
#      'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'HOST': os.environ.get('POSTGRES_HOST'),
#         'NAME': os.environ.get('POSTGRES_DB'),
#         'USER': os.environ.get('POSTGRES_USER'),
#         'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
#         'PORT': os.environ.get('POSTGRES_PORT'),
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'soinvetc_soin',
#         'USER': 'soinvetc_soinvetc',
#         'PASSWORD': 'Mejja33939085$',
#         'HOST': '',  
#         'PORT': '',
#     }
# }
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'soinvetc_soin',
#         'USER': 'soinvetc_soinvetc',
#         'PASSWORD': 'Soinvetc$2024',
#         'HOST': 'localhost',
#         'PORT': 5432,
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'soinvetc_soin',
#         'USER': 'soinvetc_soinvetc',
#         'PASSWORD': 'Mejja33939085$',
#         'HOST': 'localhost',   # MySQL works with this on cPanel
#         'PORT': '3306',
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }


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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_URL = 'https://soinvet.com'
BASE_DIR = Path(__file__).resolve().parent.parent

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#BASE_DIR / 'media'
MEDIA_URL = '/home/soinvetc/public_html/media/'
STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = 'index'

SITE_ID = 2