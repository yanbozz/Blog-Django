from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from PIL import Image
from django.core.files import File


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # specify the model to interact
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# update username and email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    # specify the model to interact
    class Meta:
        model = User
        fields = ['username', 'email']

# update image


class ProfileUpdateForm(forms.ModelForm):
    rotate = forms.FloatField(widget=forms.HiddenInput())
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    # photo = forms.ImageField(
    #     required=False,
    #     widget=forms.FileInput()
    # )

    def save(self):
        profile = super(ProfileUpdateForm, self).save()
        r = self.cleaned_data.get('rotate')
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(profile.photo.file)

        rotated_image = image.rotate(-r, expand=True)
        cropped_image = rotated_image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(profile.photo.path)
        return profile

    class Meta:
        model = Profile
        fields = ['photo', 'x', 'y', 'width', 'height', 'rotate']
