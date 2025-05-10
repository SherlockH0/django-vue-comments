# pyright: basic
from typing import Any

import magic
from django.conf import settings
from rest_framework import serializers

from backend.attachments.models import Attachment
from backend.attachments.tasks import process_attachment


class UploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = Attachment
        fields = ["file"]

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        filetype = magic.from_buffer(attrs["file"].read(), mime=True)

        if filetype not in settings.ALLOWED_MIMETYPES:
            raise serializers.ValidationError(
                {
                    "detail": f"Wrong file type. "
                    f"Allowed file types: {", ".join(settings.ALLOWED_MIMETYPES)}"
                }
            )

        if filetype in settings.ALLOWED_FILE_SIZES:
            if attrs["file"].size > settings.ALLOWED_FILE_SIZES[filetype]:
                raise serializers.ValidationError({"detail": "File too large."})

        attrs["file"].seek(0)
        attrs["filetype"] = filetype
        attrs["is_image"] = filetype.startswith("image")
        return attrs

    def save(self, **kwargs: Any) -> Any:
        attachment = super().save(**kwargs)
        process_attachment.delay(attachment.id)
        return attachment
