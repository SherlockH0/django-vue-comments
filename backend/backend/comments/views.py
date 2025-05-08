from captcha.models import CaptchaStore
from django.conf import settings
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.comments.models import Comment
from backend.comments.serializers import CommentDisplaySerializer


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )


class CommentListView(ListAPIView):
    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentDisplaySerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    pagination_class = CustomPagination
    filterset_fields = ("username", "email", "datetime_created")
    ordering_fields = ("username", "email", "datetime_created")

    @method_decorator(
        cache_page(settings.COMMENT_LIST_CACHE_TIME, key_prefix="comment_list")
    )
    def get(self, request, format=None):
        return super().get(request, format)


class CaptchaView(APIView):
    def get(self, request: Request):
        key = CaptchaStore.generate_key()
        image_url = settings.WEBSITE_ROOT + reverse(
            "captcha-image", kwargs={"key": key}
        )
        return Response(
            {
                "key": key,
                "image_url": image_url,
            }
        )
