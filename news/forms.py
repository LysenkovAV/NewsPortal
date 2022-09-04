from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'type_post',
            'title',
            'text',
            'author',
            'categories',
        ]
