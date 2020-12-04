"""form  sending mail.."""
from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    """email sending form ..."""

    name = forms.CharField(max_length=25)
    email = forms.EmailField(max_length=255)
    to = forms.EmailField(max_length=255)
    comment = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """comment form..."""

    class Meta:
        """comment models form..."""

        model = Comment
        fields = ('name', 'email', 'body')
