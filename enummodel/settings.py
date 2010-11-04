import os.path
import logging


DEBUG = False
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = DEBUG
THUMBNAIL_DEBUG = DEBUG

ADMINS = (
    ('Thom Linton', 'thom.linton@gmail.com'),
)
MANAGERS = ()
INTERNAL_IPS = (
    '127.0.0.1',
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False
USE_ETAGS = False

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    'enummodel',
    'enummodel.tests',

    'south',
]

ROOT_URLCONF = 'enummodel.tests.test_urls'
SITE_ID = 1

# Base path info
BASE_PATH = os.path.dirname(__file__)

# Testing settings
# TEST_RUNNER = "djcelery.contrib.test_runner.run_tests"

FIXTURE_DIRS = (
    os.path.join( BASE_PATH, 'fixtures' )
)
TEMPLATE_DIRS = (
    os.path.join( BASE_PATH, 'templates')
)
MEDIA_ROOT = os.path.join( BASE_PATH, 'tests', 'media' )
MEDIA_URL = '/static/'

try:
    from local_settings import *
except ImportError:
    from test_settings import *
