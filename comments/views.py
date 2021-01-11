from django.shortcuts import render, redirect

# Create your views here.
from .models import Comment
from blog.models import Posts
from .forms import CommentForm
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms


class CommentPostView(FormView):
    template_name = 'blog/posts_detail.html'
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        post = Posts.objects.get(pk=post_id)
        url = post.get_absolute_url()
        # '#' is the fragment identifier: a link to a part of a web page
        return HttpResponseRedirect(url + '#comments')

    def form_valid(self, form):
        post_id = self.kwargs['post_id']
        post = Posts.objects.get(pk=post_id)
        user = self.request.user
        comment = form.save(False)
        comment.post = post
        comment.author = user
        if form.cleaned_data['parent_comment_id']:
            parent_comment = Comment.objects.get(pk=form.cleaned_data['parent_comment_id'])
            comment.parent_comment = parent_comment
            comment.reply_to = parent_comment.author
            comment.root = parent_comment.root if parent_comment.root else parent_comment
            comment = form.save(True)
            subject = 'Someone just replied to your comment.'
            link = 'www.yanboislearning.com' + \
                '%s#div-comment-%d' % (post.get_absolute_url(), comment.root.pk)
            email = comment.reply_to.email
            if email != '':
                text = comment.body + '\n' + link
                send_mail(subject=subject, message=text, from_email=settings.EMAIL_HOST_USER,
                          recipient_list=[email], fail_silently=False)
            messages.success(self.request, f'Your reply has been posted!')
            return HttpResponseRedirect("%s#div-comment-%d" % (post.get_absolute_url(), comment.root.pk))
        comment = form.save(True)

        # comments on posts
        subject = 'You got a New Comment to your post'
        link = 'www.yanboislearning.com' + comment.post.get_absolute_url()
        email = comment.post.get_email()
        if email != '':
            text = comment.body + '\n' + link
            send_mail(subject=subject, message=text, from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[email], fail_silently=False)

        messages.success(self.request, f'Your comment has been posted!')
        return HttpResponseRedirect("%s#div-comment-%d" % (post.get_absolute_url(), comment.pk))

    def form_invalid(self, form):
        post_id = self.kwargs['post_id']
        post = Posts.objects.get(pk=post_id)
        user = self.request.user
        form = CommentForm(initial={'body': 'too long'})
        return render(self.request, self.template_name, {
            'form': form,
            'post': post,
        })
