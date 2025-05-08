from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import SET_NULL

from backend.attachments.models import Attachment

UserModel = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text = models.TextField()
    attachment = models.ForeignKey(
        Attachment, on_delete=models.SET_NULL, null=True, blank=True
    )
    parent = models.ForeignKey(
        "comments.Comment",
        related_name="children",
        related_query_name="child",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-datetime_created",)
