"""Settings specific to this application only (no Django or third party settings)."""

IN_DOCKER = False
ALLOWED_MIMETYPES = ["image/png", "image/jpeg", "image/gif", "text/plain"]

# Maximum file upload sizes (in bytes). e3 - KB, e6 - MB, e9 - GB
ALLOWED_FILE_SIZES = {
    "image/png": int(10e6),
    "image/jpeg": int(10e6),
    "image/gif": int(10e6),
    "text/plain": int(100e3),
}
POST_PROCESSORS = {
    "image/png": "backend.attachments.post_processors.ImagePostProcessor",
    "image/jpeg": "backend.attachments.post_processors.ImagePostProcessor",
    "image/gif": "backend.attachments.post_processors.ImagePostProcessor",
}

ALLOWED_TAGS = {"a", "i", "strong", "code", "br"}

MAX_IMAGE_DIMENSIONS = 320, 240
COMMENT_LIST_CACHE_TIME = 60 * 15

OTP_TOKEN_TIMEOUT = 60 * 2
