"""
Django settings for hyprfire project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-g3&jgh#03ajo(c64p90#zlch)3crljfp5pk^x_@%ls)!^859#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hyprfire_app.apps.AppConfig'
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

ROOT_URLCONF = 'hyprfire.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'hyprfire.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hyprfiredb',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'adminPostgres',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# DataFlair #Logging Information
LOGGING = {
    'version': 1,
    # disable logging; tell Django to do not disable loggers. By default, Django uses some of its own loggers.
    'disable_existing_loggers': False,

    # Loggers ####################################################################
    'loggers': {
        #one logger so all messages go through here
        'django': {
            # attach django logger with 'file' and 'console' handler
            'handlers': ['file', 'console', 'verboseFile'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': True,
        },
        # possible django.request, django.server, django.template, django.db.backends
    },

    # Handlers
    # MailHandlers and AdminEmailHandlers are possible options but over-kill for our application.
    'handlers': {
        # 'file' handler - logs to  "warning.log" file with basic detail, only writing warning, error, critical messages
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': './logs/warning.log',
            'formatter': 'basicFormat',
        },
        # 'console' handler - logs to the console with basic information, only about errors and critical messages
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
            'formatter': 'basicFormat',
        },
        # 'verboseFile' handler - logs to "verboseDebug.log" file with most details
        'verboseFile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './logs/verboseDebug.log',
            'formatter': 'verboseFormat',
        }
    },
    'formatters': {
        'basicFormat': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'verboseFormat': {
            'format': '{levelname} {asctime} {module} {lineno} {process} {processName} {thread} {threadName} {message}',
            'style': '{',
        }
    }
    # after modules are finalised, add the following to start of all modules
    # import logging
    #
    # log = logging.getLogger(__name__)
}