from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Форма для создания и редактирования публикаций."""

    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'category', 'location', 'image')


class CommentForm(forms.ModelForm):
    """Форма для создания и редактирования комментариев."""

    class Meta:
        model = Comment
        fields = ('text',)
