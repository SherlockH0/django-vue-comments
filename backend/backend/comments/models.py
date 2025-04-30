from django.contrib.auth import get_user_model
from django.db import models

from backend.attachments.models import Attachment

UserModel = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    homepage = models.URLField()
    text = models.TextField()
    attachment = models.ForeignKey(
        Attachment, on_delete=models.SET_NULL, null=True, blank=True
    )
    datetime_crated = models.DateTimeField(auto_now_add=True)
    datetime_edited = models.DateTimeField(auto_now=True)
