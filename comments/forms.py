from .models import Comment
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.translation import gettext as _


class CommentForm(ModelForm):
    parent_comment_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': _(''),
        }

        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Yeaiight...', 'wrap': 'hard', 'rows': '1', 'class': 'autoExpand', 'maxlength': '500',
                                          })
        }
