from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from .models import LikeCount, LikeRecord

# Create your views here.


def like_change(request):
    # get data
    user = request.user
    content_type = request.GET.get('content_type')
    content_type = ContentType.objects.get(moded=content_type)
    object_id = request.GET.get('object_id')
    is_like = request.GET.get('is_like')

    # process data
    if is_like:
        # to like
        like_record, created = LikeRecord.objects.get_or_create(
            content_type=content_type, object_id=object_id, user=user)
        if created:
            # never liked, then like
            like_count, created = LikeCount.objects.get_or_create(
                content_type, object_id=object_id, user=user)
            like_count.liked_num += 1
            like_count.save()
        else:
            # already liked, cannot like
            pass
    else:
        # to unlike
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user)
