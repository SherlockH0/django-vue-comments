"""Settings specific to this application only (no Django or third party settings)."""

IN_DOCKER = False
ALLOWED_MIMETYPES = ["image/png", "image/jpeg", "image/gif", "text/plain"]

# Maximum file upload sizes (in bytes). e3 - KB, e6 - MB, e9 - GB
ALLOWED_FILE_SIZES = {
    "image/png": int(2.4e6),
    "image/jpeg": int(2.4e6),
    "image/gif": int(2.4e6),
    "text/plain": int(100e3),
}

ALLOWED_TAGS = {"a", "i", "strong", "code"}

MAX_IMAGE_DIMENSIONS = 320, 240
COMMENT_LIST_CACHE_TIME = 60 * 15
