# Django settings for helidocs project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Brian Jobling', 'brian@northheli.com'),
)

MANAGERS = ADMINS
FORCE_SCRIPT_NAME=""

import iptools

INTERNAL_IPS = iptools.IpRangeList(
    '127.0.0.1',                # single ip
    '81.86.44.20',
    '195.188.251.108',
    '192.168/16',               # CIDR network block
    ('10.0.0.1', '10.0.0.19'),  # arbitrary range
)

import platform

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'helidocs_helidocs_diary',                      # Or path to database file if using sqlite3.
        'USER': 'helidocs',                      # Not used with sqlite3.
        'PASSWORD': 'dr6thEru',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}



# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SESSION_COOKIE_NAME='sessionid'

DATE_INPUT_FORMATS=('%d/%m/%y','%d/%m/%Y','%d-%m-%y','%d-%m-%Y','%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y',
'%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y',
'%B %d, %Y', '%d %B %Y', '%d %B, %Y')

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
STATIC_URL = '/static/'

if platform.system()=="Windows":
    if DEBUG:
        STATIC_DOC_ROOT = 'c:/wwwdjango/www/helidocs/static'
elif platform.system()=="Darwin":
    if DEBUG:
        STATIC_DOC_ROOT = '/Users/bhj/www/helidocs/static'
else:
    if DEBUG:
        STATIC_DOC_ROOT = '/home/technomics/venvs/helidocs/helidocs/static'

print STATIC_DOC_ROOT
# Make this unique, and don't share it with anybody.
SECRET_KEY = '>][cq$Tf\7F5ys#-6GB7~%9m!Vm5D/!.GkdK(;j1@>"_uiC0uI'
SECRET_DELETE_KEY = 'YcwY]RgYU,v0;8H{{\ZT8qo^e+a|}d0XTOlYp|8V0&yS*fJe4?'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
 #   'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
   # 'django.contrib.auth.context_processors.auth',
   #'helidocs.middleware.swfupload.SWFUploadMiddleware',
   # 'helidocs.middleware.sitelogin.SiteLogin',

    )
LOGIN_REDIRECT_URL="/"

ROOT_URLCONF = 'helidocs.urls'

if platform.system()=="Darwin":
    TEMPLATE_DIRS = (
        "/Users/bhj/www1/helidocs/templates",
        )
else:
    TEMPLATE_DIRS = (
        'templates',
        # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
    )
print TEMPLATE_DIRS

INSTALLED_APPS = (

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    #'registration',
    'helidocs.diary',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'debug_toolbar',
)


DEBUG_TOOLBAR_CONFIG={'INTERCEPT_REDIRECTS':False}

try:
   from local_settings import *
except:
   pass
