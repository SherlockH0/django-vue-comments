import logging

from celery import shared_task

from backend.attachments.models import Attachment

from .utils import get_post_processor_for_filetype

logger = logging.getLogger(__name__)


@shared_task
def process_attachment(attachment_id: int) -> str:
    try:
        attachment = Attachment.objects.get(pk=attachment_id)
    except Attachment.DoesNotExist:
        return f"Attachment with ID {attachment_id} does not exist."

    try:
        processor_class = get_post_processor_for_filetype(attachment.filetype)

        if not processor_class:
            return (
                f"Post-processing not supported for filetype '{attachment.filetype}'."
            )
        processor = processor_class()
        processed_file = processor.process(attachment.file, attachment.filetype)

        attachment.file.delete(save=False)
        attachment.file = processed_file
        attachment.save()

        return "File processed successfully."
    except Exception as e:
        logger.exception("Error during file post-processing.")
        return f"Failed to process file: {str(e)}"
