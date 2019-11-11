# articles/forms.py
from django import forms
from .models import Article, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label="제목",
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'title',
            'placeholder': 'Enter the title',
        })
    )

    class Meta:
        model = Article
        fields = "__all__"

# class ArticleForm(forms.Form):
#     # max_length/ min_length
#     title = forms.CharField(
#         max_length=10,
#         label="제목",
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'my-title',
#                 'placeholder': 'Enter the title!',
#             }
#         )
#     )
#     content = forms.CharField(
#         min_length=20, 
#         widget=forms.Textarea(
#             attrs={
#                 'class': 'my-content',
#                 'placeholder': 'Enter the content!',
#                 'row': 5,
#                 'cols': 50,
#             }
#         )
#     )