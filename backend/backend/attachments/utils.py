import importlib

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .post_processors import FilePostProcessor


def get_post_processor_for_filetype(filetype: str) -> type[FilePostProcessor] | None:
    """Get the file processor from settings for the give filetype.

    Raises:
        ImproperlyConfigured: If post-processor given in settings
            is not a subclass of FilePostProcessor.

    """
    path: str | None = settings.POST_PROCESSORS.get(filetype, None)
    if not path:
        return
    module_name, class_name = path.rsplit(".", 1)
    module = importlib.import_module(module_name)

    processor_class = getattr(module, class_name)
    if not issubclass(processor_class, FilePostProcessor):
        raise ImproperlyConfigured(
            "Post-processor should inherit a FilePostProcessor class."
        )
    return processor_class
