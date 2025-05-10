SECRET_KEY = "django-insecure-k5z$l1h+3*@lqc#sgxeucq^=(c&gab%_y14cpp&nx5+7m^ou5$"
DEBUG = True

CELERY_BROKER_URL = "redis://localhost:6379/1"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://localhost:6379/2",
    }
}

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "your_cloud_name",
    "API_KEY": "your_api_key",
    "API_SECRET": "your_api_secret",
}
# Can also be set via env variables: https://pypi.org/project/django-cloudinary-storage/
