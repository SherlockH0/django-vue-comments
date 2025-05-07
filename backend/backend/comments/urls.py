from django.urls import path

from backend.comments.views import CommentListView

urlpatterns = [
    path("comments/", CommentListView().as_view(), name="comments-list"),
]
