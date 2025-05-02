from rest_framework.generics import ListAPIView

from backend.comments.models import Comment
from backend.comments.serializers import CommentSerializer


class CommentListView(ListAPIView):
    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentSerializer
    filterset_fields = ("parent", "datetime_created")
