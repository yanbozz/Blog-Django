from django.urls import path, include
from django.conf.urls import url, include
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    AboutView,
)
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', AboutView.as_view(), name='blog-about'),
    url(r'', include('comments.urls', namespace='comment'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# <app>/<model>_<viewtype>.html
# blog/posts_list.html
