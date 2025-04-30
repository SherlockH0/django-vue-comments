from django.urls import path

from backend.attachments.views import UploadAttachmentView

urlpatterns = [
    path("upload/", UploadAttachmentView.as_view()),
]
