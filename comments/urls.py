from django.urls import path
from .views import CommentPostView

app_name = "comments"

urlpatterns = [path('post/<int:post_id>/postcomment',
                    CommentPostView.as_view(), name='postcomment')]
