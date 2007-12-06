#   Copyright 2007 Casey Durfee
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

ugettext = lambda s: s

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)
DEBUG= True
TEMPLATE_DEBUG = DEBUG
ADMINS = ( )
MANAGERS = ADMINS

#DATABASE_ENGINE = 'postgresql'
#DATABASE_NAME = 'fbo'
#DATABASE_USER = 'fbo'
#DATABASE_PASSWORD = 'fbo'
#DATABASE_HOST = 'localhost'
#DATABASE_PORT = '5432'

TIME_ZONE = "PST8PDT"

#CACHE_BACKEND = 'simple:///'
#CACHE_BACKEND = 'locmem:///'
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
#CACHE_MIDDLEWARE_SECONDS = 3600

DEFAULT_CHARSET='utf-8'
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('fr', ugettext('French')),
    ('en', ugettext('English')),
)

SITE_ID = 1 
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'

# You should set this to something long and cryptic
SECRET_KEY = ''

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    #"django.middleware.cache.CacheMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.doc.XViewMiddleware",
    "django.middleware.gzip.GZipMiddleware",
)

ROOT_URLCONF = 'helios.urls'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'django.contrib.sessions',
    'helios.discovery',
    'helios.catalog',
)
