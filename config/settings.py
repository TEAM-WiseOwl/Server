from pathlib import Path
import os
import local_settings 
from datetime import timedelta
from celery.schedules import crontab
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = local_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'accounts.User'
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_apscheduler',

    "rest_framework",
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',

    "corsheaders",
    "whitenoise.runserver_nostatic",

    'dj_rest_auth',
    'dj_rest_auth.registration',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    "accounts",
    "notices",
    "requirements",
    "products",
    "payments",
    "facilities",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = local_settings.DATABASES

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }
# db_from_env = dj_database_url.config(conn_max_age = 500)

# DATABASES['default'].update(db_from_env)

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' #?

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"  # Default

# SCHEDULER_DEFAULT = True => 주기적인 작업 수행이 필요할 때 사용(로그 파일 청소 등)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.permissions.AllowAny', 
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', # 인증된 사용자만 접근
        # 'rest_framework.permissions.IsAdminUser', # 관리자만 접근
        # 'rest_framework.permissions.AllowAny', # 누구나 접근
    ),
}

REST_USE_JWT = True


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'user_id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

## 세션 만료 관리
# 브라우저 닫으면 삭제 (default False)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# 비활동 최대 기한 (default 2주)
SESSION_COOKIE_AGE = 86400

# https에서만 세션 쿠키가 전송 (default false) https 배포 시 true로
SESSION_COOKIE_SECURE = False

ACCOUNT_EMAIL_REQUIRED = True            # email 필드 사용 o
ACCOUNT_USERNAME_REQUIRED = False         # username 필드 사용 o
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

GOOGLE_CLIENT_ID = local_settings.GOOGLE_CLIENT_ID
GOOGLE_SECRET = local_settings.GOOGLE_SECRET
GOOGLE_REDIRECT = local_settings.GOOGLE_REDIRECT
GOOGLE_CALLBACK_URL = local_settings.GOOGLE_CALLBACK_URI
GOOGLE_SCOPE_USERINFO = local_settings.GOOGLE_SCOPE_USERINFO

##CORS
# CORS_ORIGIN_WHITELIST = []
CORS_ORIGIN_ALLOW_ALL=True # <- 모든 호스트 허용
CORS_ALLOW_CREDENTIALS = True # <-쿠키가 cross-site HTTP 요청에 포함될 수 있다

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    #만약 허용해야할 추가적인 헤더키가 있다면(사용자정의 키) 여기에 추가하면 됩니다.
]

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

APPEND_SLASH = False
CORS_PREFLIGHT_MAX_AGE = 86400

CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'crawl-posts-every-30-minutes': {
        'task': 'notices.crawler.crawl_notices',
        'schedule': crontab(minute='*/30'),  # 30분마다 크롤링
    },
}