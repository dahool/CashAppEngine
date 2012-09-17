# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import *

import os

PROJECT_PATH = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))

VERSION = "0.9.1"
APPLICATION = "Cash Manager"
MOBILE_VERSION = "1.1.0"

# Activate django-dbindexer for the default database
DATABASES['native'] = DATABASES['default']
DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
AUTOLOAD_SITECONF = 'indexes'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

INSTALLED_APPS = (
#    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'djangotoolbox',
    'dbindexer',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'pycash.cash',
    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
)

MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pycash.cash.loginrequiredmiddleware.LoginRequiredMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)

AUTHENTICATION_BACKENDS = ('pycash.settings_auth.SettingsAuthBackend',
                           'django.contrib.auth.backends.ModelBackend',)
                           
LOGIN_URL = '/login'
LOGIN_EXEMPT_URLS = '/token'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login'

ADMIN_LOGIN='admin'
ADMIN_PWD='admin'

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

MEDIA_ROOT = os.path.join(PROJECT_PATH,'media_store')
STATIC_ROOT = os.path.join(PROJECT_PATH, 'media')

ADMIN_MEDIA_PREFIX = '/media/admin/'
MEDIA_URL = '/site_store/'
STATIC_URL = '/media/'
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'pycash', 'templates'),)

USE_GOOGLE_CAL = False

ROOT_URLCONF = 'urls'
