from django.urls import path

from backend.comments.views import CaptchaView, CommentListView

urlpatterns = [
    path("", CommentListView().as_view(), name="comments-list"),
    path("captcha/", CaptchaView().as_view(), name="get-captcha"),
]
