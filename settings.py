# Django settings for myweb project.
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

#DEBUG = True
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'jsjt_db',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'jsjt',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh_CN'

# 
SITE_ID = 1
# 
# LANGUAGES = (
#     #('en', 'English'),
#     ('zh_CN', 'Chinese'),
# ) 

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
if not hasattr(globals(), 'SECRET_KEY'):
    SECRET_FILE = os.path.join(PROJECT_ROOT, 'secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            from random import choice
            import string
            symbols = ''.join((string.lowercase, string.digits, string.punctuation ))
            SECRET_KEY = ''.join([choice(symbols) for i in range(50)])
            secret = file(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            raise Exception('Please create a %s file with random characters to generate your secret key!' % SECRET_FILE)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.middleware.csrf.CsrfResponseMiddleware',
    #'django_authopenid.middleware.OpenIDMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'apps.jsjtbb.middleware.LastLoginMiddleware',
    'apps.jsjtbb.middleware.UsersOnline',
    #api
    # 'api.crossdomain.XsSharing',
)

ROOT_URLCONF = 'urls'

TEMPLATE_ROOT = os.path.join(PROJECT_ROOT, 'templates')

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # 'g:/jsjt/myweb/templates'
    TEMPLATE_ROOT
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'django.contrib.humanize',
    # 'registration',
    #'django_authopenid',
    'djapian',
    # 'messages',
    'apps.news',
    'apps.lessons',
    'apps.contacts',
    'apps.accounts',
    'apps.location',
    'apps.ranking',
    'apps.jsjtbb',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    #'django_authopenid.context_processors.authopenid',
    'apps.jsjtbb.context_processors.forum_settings',
)

# accounts
AUTH_PROFILE_MODULE = 'apps.accounts.UserProfile'

#email 
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'litekok@gmail.com'
# EMAIL_HOST_PASSWORD = '!(&*$!*'
# EMAIL_PORT = 587

# ranking
LOG_FILE = "myweb.log"
LOG_LEVEL = 20  #CRITICAL 50 ERROR 40 WARNING 30 INFO 20 DEBUG 10 

# Djapian settings
DJAPIAN_DATABASE_PATH = os.path.join(PROJECT_ROOT, 'djapian_db')

# Account settings
ACCOUNT_ACTIVATION_DAYS = 10
LOGIN_REDIRECT_URL = '/forum/'
LOGIN_URL = '/accounts/login/'

#Cache settings
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# XS_SHARING_ALLOWED_ORIGINS = '*'
# XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE', 'HEAD']

#import pdb
#pdb.set_trace()

