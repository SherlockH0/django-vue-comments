# pyright: basic
import bleach
from django.conf import settings
from rest_framework import serializers

from backend.comments.models import Comment


class ChildrenListingField(serializers.RelatedField):
    def to_representation(self, value):
        return CommentSerializer(value).data


class AttachmentField(serializers.RelatedField):
    def to_representation(self, value):
        return value.file.url


class CommentSerializer(serializers.ModelSerializer):
    children = ChildrenListingField(many=True, read_only=True)
    attachment = AttachmentField(read_only=True)

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
