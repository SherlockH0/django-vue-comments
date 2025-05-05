import io
import os

from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image

from backend.attachments.models import Attachment


@shared_task
def process_attachment(attachment_id: int) -> str:
    attachment = Attachment.objects.get(pk=attachment_id)
    if not attachment.is_image:
        return "File is not an image."

    image = Image.open(attachment.file)

    if (
        image.height <= settings.MAX_IMAGE_DIMENSIONS[0]
        and image.width <= settings.MAX_IMAGE_DIMENSIONS[1]
    ):
        return "File already satisfies requirements."

    image.thumbnail(settings.MAX_IMAGE_DIMENSIONS)
    new_image = io.BytesIO()

    image.save(new_image, attachment.filetype.split("/")[-1].upper())

    new_image = ContentFile(
        new_image.getvalue(), str(os.path.basename(attachment.file.name))
    )

    attachment.file.delete()
    attachment.file = new_image
    attachment.save()

    return "File resized successfully"
