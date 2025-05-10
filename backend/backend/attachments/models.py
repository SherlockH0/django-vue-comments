from django.db import models


class Attachment(models.Model):
    file = models.ImageField(
        upload_to="uploads/%Y/%m/%d/",
        null=True,
        blank=True,
    )
    filetype = models.CharField(max_length=12)
    is_image = models.BooleanField()
    datetime_uploaded = models.DateField(auto_now_add=True)
