from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    # CASCADE: if the user deleted, also delete the profile, but reversely not
    # OneToOneFiled
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='default.jpg',
                              upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kawrgs):
    #     super().save(*args, **kawrgs)
    #
    #     # open image of the current instance and resize it
    #     img = Image.open(self.photo.path)
    #
    #     if img.height > 200 or img.width > 200:
    #         output_size = (200, 200)
    #         img.thumbnail(output_size)
    #         img.save(self.photo.path)
