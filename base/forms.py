from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        label="Post Tags",
        help_text="Type comma separated post tags",
        required=False,
    )

    class Meta:
        model = Post
        fields = ["title", "description", "image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["description"]
