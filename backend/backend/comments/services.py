from backend.comments.serializers import CommentDisplaySerializer, CommentSerializer


def create_comment(data: dict) -> dict:
    serializer = CommentSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    instance = serializer.save()
    return CommentDisplaySerializer(instance).data
