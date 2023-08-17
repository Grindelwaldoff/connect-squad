"""
Django settings for accmarks project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

# ALLOWED_HOSTS = ['knouna7x.beget.tech']
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account.apps.AccountConfig',
    'django.contrib.admin',
    'shop.apps.ShopConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'inpage.apps.InpageConfig',
    'django_filters'
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

ROOT_URLCONF = 'accmarks.urls'

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
                'cart.context_processors.cart',
                'inpage.context_processors.header',
            ],
        },
    },
]

WSGI_APPLICATION = 'accmarks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = reverse_lazy('inpage:index')
LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CART_SESSION_ID = 'cart'

MAX_LENGTH_CHAR = 200
MAX_LENGTH_DESC = 200
MAX_LENGTH_INT = 10
MAX_LENGTH_ADV = 10000

METHODS = (
    ('scum', 'Фишинг'),
    ('resell', 'Перепродажа'),
    ('mine', 'Продажа своего')
)

GAMES = ((), ())

METHODS = (
    ('scum', 'Фишинг'),
    ('resell', 'Перепродажа'),
    ('mine', 'Продажа своего')
)

EMAIL_ACCESS = (
    ('AUTO', 'Авторег'),
    ('ORIGINAL', 'Родная'),
    ('NO', 'Без почты')
)

SEX = (
    ('man', 'Мужской'),
    ('woman', 'Женский'),
    (None, 'Неизвестно')
)

LINKS = {
    'telegram': 'shop/tg.html',
    'whatsapp': 'shop/whatsApp.html',
    # 'steam': 'shop/steam.html'
    'instagram': 'shop/instagram.html',
    'vk': 'shop/vk.html',
    # 'tiktok': 'shop/tiktok.html',
    # 'ttv': 'shop/twitch.html',
    'ok': 'shop/ok.html',
    # 'facebook': 'shop/facebook.html',
    # 'mail': 'shop/mail.html',
    # 'twitter': 'shop/twitter.html',
    # 'youtube': 'shop/youtube.html',
    # 'discord': 'shop/discord.html',
    None: 'error/404.html'
}

EMAIL_DOMAINS = (
    ('yandex', '@yandex'),
    ('gmail', '@gmail'),
    ('rambler', '@rambler'),
    ('mail', '@mail'),
)

COUNTRY_CHOICES = (
    ('RU', 'Россия'),
    ('US', 'США'),
    ('KZ', 'Казахстан')
)

BOOL_PARAMS = (
    ('premium', 'Премиум'),
    ('spam_block', 'Спам блок'),
    ('password', 'Пароль'),
    ('cookies', 'Куки'),
    ('binding_phone', 'Привязка к телефону'),
)

PSIF_PARAMS = (
    ('channels', 'Кол-во каналов'),
    ('groups', 'Кол-во групп'),
    ('chats', 'Кол-во чатов'),
    ('admin_chats', 'Кол-во админ чатов'),
    ('guaranty', 'Срок гарантии'),
    ('posts', 'Кол-во постов'),
    ('age', 'Возраст'),
    ('friends', 'Друзей')
)

PIF_PARAMS = (
    ('chat_subs', 'Кол-во подписчиков в чатах'),
    ('general_balance', 'Баланс на аккаунте'),
    ('subs', 'Кол-во Подписчиков'),
    ('votes', 'Кол-во голосов'),
)

PARAMS_OF_DIFFERENT_CAT = {
    'telegram': (
        PSIF_PARAMS[0], PSIF_PARAMS[1], PSIF_PARAMS[2],
        PSIF_PARAMS[3], BOOL_PARAMS[0], PIF_PARAMS[0],
        BOOL_PARAMS[1], BOOL_PARAMS[2]
    ),
    'whatsapp': (
        PSIF_PARAMS[0], PSIF_PARAMS[1], PSIF_PARAMS[2],
        PSIF_PARAMS[3], BOOL_PARAMS[0],
        BOOL_PARAMS[1], BOOL_PARAMS[2]
    ),
    'ok': (
        PSIF_PARAMS[-2], PIF_PARAMS[-1], PIF_PARAMS[-2],
        PSIF_PARAMS[1], PSIF_PARAMS[-1],
    ),
    'vk': (
        PSIF_PARAMS[-2], PIF_PARAMS[-1], PIF_PARAMS[-2],
        PSIF_PARAMS[1], PSIF_PARAMS[-1],
    ),
}
