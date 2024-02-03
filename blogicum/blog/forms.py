from django import forms

from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'is_published',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
