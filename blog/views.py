from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from .models import Posts
from comments.models import Comment
from comments.forms import CommentForm


# class base view
class PostListView(ListView):
    model = Posts
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    # make newest post on the top
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Posts
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Posts.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Posts

    def get_context_data(self, **kwargs):
        post_id = int(self.kwargs[self.pk_url_kwarg])
        comment_form = CommentForm()
        user = self.request.user
        comments = Comment.objects.filter(post_id=post_id, parent_comment=None)
        kwargs['comment_list'] = comments
        kwargs['comment_count'] = len(comments) if comments else 0
        kwargs['form'] = comment_form
        kwargs['next_blog'] = Posts.objects.filter(
            date_posted__gt=self.object.date_posted).first()
        kwargs['previous_blog'] = Posts.objects.filter(
            date_posted__lt=self.object.date_posted).last()

        return super(PostDetailView, self).get_context_data(**kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    fields = ['title', 'content']

    def form_valid(self, form):
        # set the author equal to current logged in user
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # check if the author who is trying to update equal to the post user
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class AboutView(TemplateView):
    template_name = 'blog/about.html'
