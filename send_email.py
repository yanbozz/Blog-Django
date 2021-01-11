# from django.conf import settings
# from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail


send_mail(
    'Subject here',
    'Here is the message.',
    'no-reply@yanboislearning.com',
    ['yanbozhao1994@gmail.com'],
    fail_silently=False,
)
