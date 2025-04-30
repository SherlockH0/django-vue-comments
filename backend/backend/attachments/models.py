from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models


class Attachment(models.Model):
    file = models.FileField(
        upload_to="uploads/%Y/%m/%d/",
        validators=[FileExtensionValidator(settings.ALLOWED_EXTENSIONS)],
    )
    datetime_uploaded = models.DateField(auto_now_add=True)
