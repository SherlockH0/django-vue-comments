from django.contrib.auth.models import AbstractUser

from backend.comments.serializers import (
    ComentCreateSerializer,
    CommentDisplaySerializer,
)


def create_comment(user: AbstractUser, data: dict) -> dict:
    data.update({"user": user.pk})
    serializer = ComentCreateSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    return CommentDisplaySerializer(instance).data
