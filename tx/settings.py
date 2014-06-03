"""
Django settings for tx project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#root = os.path.dirname(os.path.dirname(__file__)).replace('\\','/')
#MEDIA_ROOT = root + '/../media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATIC_DIRS = (os.path.join(BASE_DIR, u'static'),)

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'), )

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
SECRET_KEY = '7-)l_n0-y^e%-4!0ugm8w=s!dt-037a3h72n^#isu&uxj+m8w-'
ALLOWED_HOSTS = [u'localhost', u'176.ip-92-222-19.eu']


# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'main',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tx.urls'

WSGI_APPLICATION = 'tx.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psygcopg2',
#        'NAME': 'daqkph7qnc6bhv',
#        'USER': 'nemfikadudwjsz',
#        'PASSWORD': 'Gr9gqlwARMacBLpeo3nPhbe8Fz',
#        'PORT': 5432,
#        'HOST': 'ec2-54-204-24-154.compute-1.amazonaws.com',
#    }
#}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/


LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
