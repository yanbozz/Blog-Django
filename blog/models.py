from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Posts(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    # on_delete: delete the posts when the user iteself is deleted, only onw-way straight
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # redirect to the post detail page after the new post is created
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_email(self):
        return self.author.email
