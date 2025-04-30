# pyright: basic
from rest_framework.serializers import FileField, ModelSerializer

from backend.attachments.models import Attachment


class UploadSerializer(ModelSerializer):
    file = FileField()

    class Meta:
        model = Attachment
        fields = ["file"]

    def validate_file(self, value):
        # TODO
        return value
