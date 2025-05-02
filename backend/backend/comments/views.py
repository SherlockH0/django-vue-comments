from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from backend.comments.models import Comment
from backend.comments.serializers import CommentSerializer


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )


class CommentListView(ListAPIView):
    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    pagination_class = CustomPagination
    filterset_fields = ("username", "email", "datetime_created")
    ordering_fields = ("username", "email", "datetime_created")
