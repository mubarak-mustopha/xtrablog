import re
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

    @classmethod
    def _normalize_tags(self, tag_names):
        """
        Given a list of tag_names
        Makes sure tag label starts and ends with alphabets.
        Capitalizes tag label
        Example:
            >>> PostForm._normalize_tags(["  design","@design", "___design"])
                ['Design', 'Design', 'Design']
        """
        pattern = re.compile(r"^[^a-z]+|[^a-z]+$", re.I)
        normalized_tags = []
        for tag_name in tag_names:
            normalized_tags.append(re.sub(pattern, "", tag_name).capitalize())
        return normalized_tags

    def clean_tags(self):
        tags = self.cleaned_data["tags"]
        normalized_tags = self._normalize_tags(tags.split(","))
        return [n_tag for n_tag in normalized_tags if n_tag != ""]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["description"]


class PostUpdateForm(PostForm):
    initial_tags = forms.CharField(widget=forms.HiddenInput)

    def clean_initial_tags(self):
        init_tags = self.cleaned_data["initial_tags"]
        normalized_tags = super()._normalize_tags(init_tags.split(","))
        return [n_tag for n_tag in normalized_tags if n_tag != ""]
