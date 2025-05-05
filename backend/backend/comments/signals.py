import logging

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from backend.comments.models import Comment

logger = logging.getLogger(__name__)


@receiver([post_save, post_delete], sender=Comment)
def clean_cache(*args, **kwargs):
    if hasattr(cache, "delete_pattern"):
        cache.delete_pattern("*comment_list*")  # type: ignore
    else:
        logger.warning(
            "You are not using django_redis for caching! The cache will not be cleared on model changes."
        )
