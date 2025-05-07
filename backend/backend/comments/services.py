from backend.comments.serializers import (
    ComentCreateSerializer,
    CommentDisplaySerializer,
)


def create_comment(data: dict) -> dict:
    serializer = ComentCreateSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    return CommentDisplaySerializer(instance).data
