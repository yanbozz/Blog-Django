from django.db import models
from django.contrib.auth.models import User
from blog.models import Posts


# Create your models here.


class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    # foreign key piont to comment itself
    parent_comment = models.ForeignKey(
        'self', verbose_name='parent_comment', blank=True, null=True, on_delete=models.CASCADE)
    root = models.ForeignKey('self', related_name='root_comment', blank=True,
                             null=True, on_delete=models.DO_NOTHING)
    reply_to = models.ForeignKey(User, related_name='replies', blank=True,
                                 null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def approved(self):
        self.approved = True
        self.save()

    class Meta:
        ordering = ['-id']
        verbose_name = "Comment"
        verbose_name_plural = verbose_name
        get_latest_by = 'created'

    def __str__(self):
        return self.body

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
