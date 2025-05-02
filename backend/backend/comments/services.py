from backend.comments.serializers import CommentSerializer


def create_comment(data: dict) -> dict:
    serializer = CommentSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data
