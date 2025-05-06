# pyright: basic
import os

import bleach
from django.conf import settings
from rest_framework import serializers

from backend.comments.models import Comment


class ChildrenListingField(serializers.RelatedField):
    def to_representation(self, value):
        return CommentSerializer(value).data


class CommentSerializer(serializers.ModelSerializer):
    children = ChildrenListingField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "parent",
            "username",
            "email",
            "text",
            "datetime_created",
            "datetime_edited",
            "attachment",
            "children",
        )

    def validate_text(self, value):
        return bleach.clean(value, tags=settings.ALLOWED_TAGS)


class AttachmentField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "url": value.file.url,
            "image": value.is_image,
            "name": os.path.basename(value.file.name),
        }


class CommentDisplaySerializer(CommentSerializer):
    attachment = AttachmentField(read_only=True)
