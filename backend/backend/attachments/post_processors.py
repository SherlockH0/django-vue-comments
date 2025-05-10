"""Post-processing handlers for uploaded attachments.

Provides an abstract interface and concrete implementations for processing various file types.
"""

import io
import os
from abc import ABC, abstractmethod

from django.conf import settings
from django.core.files.base import ContentFile, File
from django.db.models.fields.files import FieldFile
from PIL import Image, UnidentifiedImageError


class FilePostProcessor(ABC):
    """Abstract base class for file post-processors."""

    @abstractmethod
    def process(self, file: FieldFile, filetype: str) -> ContentFile | File:
        """Process the file and return a new or modified version."""
        ...


class ImagePostProcessor(FilePostProcessor):
    """Resizes images exceeding max dimensions."""

    def process(self, file: FieldFile, filetype: str) -> ContentFile | File:
        """Resize the image if it exceeds MAX_IMAGE_DIMENSIONS.

        Args:
            file: The uploaded image file.
            filetype: MIME type of the image.

        Returns:
            Resized image as ContentFile or original if within limits.

        Raises:
            ValueError: If the file is not a valid image.
        """
        try:
            image = Image.open(file)
        except UnidentifiedImageError:
            raise ValueError("Invalid image file")

        max_width, max_height = settings.MAX_IMAGE_DIMENSIONS

        if image.height <= max_height and image.width <= max_width:
            return file

        image.thumbnail((max_width, max_height))

        with io.BytesIO() as buffer:
            format = filetype.split("/")[-1].upper()
            filename = str(os.path.basename(file.name))

            image.save(buffer, format)

            return ContentFile(buffer.getvalue(), filename)
