# -----------------------------------------------------------------------------
#    karajlug.org
#    Copyright (C) 2010  karajlug community
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------
import imp
import os
import sys

ON_OPENSHIFT = False
if 'OPENSHIFT_REPO_DIR' in os.environ:
    ON_OPENSHIFT = True

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
if ON_OPENSHIFT:
    DEBUG = bool(os.environ.get('DEBUG', False))
    if DEBUG:
        print("WARNING: The DEBUG environment is set to True.")
else:
    DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Keyvan Hedayati', 'k1.hedayati93@gmail.com'),
)

MANAGERS = ADMINS

if ON_OPENSHIFT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'tehpug',
            'USER': os.environ.get('OPENSHIFT_POSTGRESQL_DB_USERNAME'),
            'PASSWORD': os.environ.get('OPENSHIFT_POSTGRESQL_DB_PASSWORD'),
            'HOST': os.environ.get('OPENSHIFT_POSTGRESQL_DB_HOST'),
            'PORT': os.environ.get('OPENSHIFT_POSTGRESQL_DB_PORT'),
        }
    }
else:
    DATABASES = {
        'sqlite': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJECT_DIR, 'sqlite3.db'),
        },
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'tehpug',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': 5432,
        }
    }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.

TIME_ZONE = 'Asia/Tehran'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fa'

_ = lambda s: s

LANGUAGES = [
    ["fa", _("Persian")],
    ["en", _("English")],
]

SITE_ID = 2

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.environ.get('OPENSHIFT_DATA_DIR', '')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/upload/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', ''), 'statics')
STATIC_ROOT = os.path.join(PROJECT_DIR, '..', 'static')
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, '..', 'statics'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
default_keys = {
    'SECRET_KEY': 'as#jgh[cn]@%^sKHJkh9&*(&987(^%^&65$GJB<Psodqlwllkasd]))'
}

# Replace default keys with dynamic values if we are in OpenShift
if ON_OPENSHIFT:
    # imp.find_module('openshiftlibs')
    import openshiftlibs
    use_keys = openshiftlibs.openshift_secure(default_keys)
else:
    use_keys = default_keys

# Make this unique, and don't share it with anybody.
SECRET_KEY = use_keys['SECRET_KEY']

DBBACKUP_STORAGE = 'dbbackup.storage.dropbox_storage'
if ON_OPENSHIFT:
    DBBACKUP_TOKENS_FILEPATH = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', ''), 'tokens')
    sys.path.insert(0, os.environ.get('OPENSHIFT_DATA_DIR', ''))
    DBBACKUP_SERVER_NAME = 'production'
else:
    DBBACKUP_TOKENS_FILEPATH = os.path.join(PROJECT_DIR, 'tokens')
    DBBACKUP_SERVER_NAME = 'develop'

from secrets import DBBACKUP_DROPBOX_APP_KEY, DBBACKUP_DROPBOX_APP_SECRET

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

LEAF_URLCONF = 'tehpug.urls'
ROOT_URLCONF = 'multilang.urls'

# Python dotted path to the WSGI application used by Django's runserver.
# WSGI_APPLICATION = 'tehpug.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, '..', 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'modeltranslation',                   # If you want to use the admin integration, modeltranslation must be put before django.contrib.admin.
    'django.contrib.admin',
    'django_markdown',
    'south',
    'dbbackup',
    "page",
    "news",
    "faq",
    "projects",
    "viewhelper",
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    "tehpug.context_processors.info",
)

BOOK_IN_PAGE = 5
VERSION = "0.48.19"
NEWS_LIMIT = 10
AUTH_PROFILE_MODULE = 'members.Member'

APPEND_SLASH = True
LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, "../locale"),
)

ALLOWED_HOSTS = (
    ".rhcloud.com",
    "127.0.0.1:7020",
    "www.tehpug.ir",
    "tehpug.ir",
    "127.0.0.1",
    'django-dbbackup'
)

DBBACKUP_POSTGRESQL_BACKUP_COMMANDS = [['pg_dump', '-O', '--username={adminuser}', '--host={host}', '--port={port}', '{databasename}', '>']]

MODELTRANSLATION_FALLBACK_LANGUAGES = ('fa', 'en')
