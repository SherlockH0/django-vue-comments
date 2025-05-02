from celery import shared_task
from django.conf import settings
from PIL import Image


@shared_task
def resize_image(path: str) -> str:
    image = Image.open(path)

    if (
        image.height > settings.MAX_IMAGE_DIMENSIONS[0]
        or image.width > settings.MAX_IMAGE_DIMENSIONS[1]
    ):
        image.thumbnail(settings.MAX_IMAGE_DIMENSIONS)
        image.save(path)
        return "File resized successfully"

    return "File already satisfies requirements."
