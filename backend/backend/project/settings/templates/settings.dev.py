SECRET_KEY = "django-insecure-k5z$l1h+3*@lqc#sgxeucq^=(c&gab%_y14cpp&nx5+7m^ou5$"
DEBUG = True

CELERY_BROKER_URL = "redis://localhost:6379"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://localhost:6379",
    }
}
