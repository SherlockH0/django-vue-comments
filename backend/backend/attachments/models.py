import celery
from django.db import models

from backend.attachments.tasks import resize_image


class Attachment(models.Model):
    file = models.FileField(
        upload_to="uploads/%Y/%m/%d/",
    )
    filetype = models.CharField(max_length=12)
    is_image = models.BooleanField()
    resized = models.BooleanField(default=False)
    datetime_uploaded = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if not self.resized:
            if self.is_image:
                resize_image.delay(self.file.path)
