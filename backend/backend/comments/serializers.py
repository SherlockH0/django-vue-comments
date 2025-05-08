# pyright: basic
import os
from typing import Any

import bleach
import tidylib
from captcha.serializers import CaptchaModelSerializer
from django.conf import settings
from rest_framework import serializers

from backend.comments.models import Comment


class BaseCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "parent",
            "username",
            "email",
            "text",
            "attachment",
        )

    def validate_text(self, value: str):
        html = value.replace("\n", "<br>")
        tidy_html, _ = tidylib.tidy_fragment(html)
        clean_html = bleach.clean(tidy_html, tags=settings.ALLOWED_TAGS, strip=True)
        return clean_html


class ComentCreateSerializer(CaptchaModelSerializer, BaseCommentSerializer):
    class Meta:
        model = Comment
        fields = BaseCommentSerializer.Meta.fields + (
            "captcha_code",
            "captcha_hashkey",
        )

    def create(self, validated_data: dict[str, Any]) -> Any:
        validated_data.pop("captcha_code")
        validated_data.pop("captcha_hashkey")
        return super().create(validated_data)

    def is_valid(self, *args, **kwargs) -> bool:
        try:
            return super().is_valid(*args, **kwargs)
        except serializers.ValidationError as e:
            if "CAPTCHA" in str(e):
                raise serializers.ValidationError({"captcha": [e.detail["error"]]})
            raise e


class ChildrenListingField(serializers.RelatedField):
    def to_representation(self, value):
        return CommentDisplaySerializer(value).data


class AttachmentField(serializers.RelatedField):
    def to_representation(self, value):
        website_root = settings.WEBSITE_ROOT
        return {
            "url": website_root + value.file.url,
            "image": value.is_image,
            "name": os.path.basename(value.file.name),
        }


class CommentDisplaySerializer(BaseCommentSerializer):
    attachment = AttachmentField(read_only=True)
    children = ChildrenListingField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = BaseCommentSerializer.Meta.fields + (
            "children",
            "datetime_created",
            "datetime_edited",
        )
