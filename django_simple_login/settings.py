# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

#
# Simple Login
# Copyright (C) 2016 byteShaft
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os

from django_simple_login.helpers import ConfigHelpers

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.expanduser('~/sample_config.ini')
config_helpers = ConfigHelpers(CONFIG_FILE)
SECRET_KEY = '*e-fod9wl!k0x=9%@*=6sf(=@i99x_o#lw)z$+80!ineak18xp'
DEBUG = config_helpers.get_debug_setting()

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'simple_login',
    'sample_app',
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

ROOT_URLCONF = 'django_simple_login.urls'
AUTH_USER_MODEL = 'sample_app.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'simple_login.utils.authentication.TokenAuthentication',
    )
}

WSGI_APPLICATION = 'django_simple_login.wsgi.application'
APP_NAME = 'Simple Login'
# Supported methods email and sms
OTP_METHODS = ['EMAIL']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

EMAIL_USE_TLS = True
EMAIL_HOST = config_helpers.get_email_credential_by_key('host')
EMAIL_HOST_USER = config_helpers.get_email_credential_by_key('email')
EMAIL_HOST_PASSWORD = config_helpers.get_email_credential_by_key('password')
EMAIL_PORT = config_helpers.get_email_credential_by_key('port')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_AUTH_METHOD = 'email'

TWITTER_CONSUMER_KEY = config_helpers.get_twitter_cred_by_key('CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = config_helpers.get_twitter_cred_by_key('CONSUMER_SECRET')
AUTH_USER_SERIALIZER = 'sample_app.serializers.UserSerializer'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
