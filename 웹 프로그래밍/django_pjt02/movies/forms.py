from django import forms
from .models import Movie, Rating

class MovieForm(forms.ModelForm):
    title = forms.CharField(
        label="영화 제목",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'title',
            'placeholder': '제목을 입력하세요.'
        })
    )

    class Meta:
        model = Movie
        fields = ('title', 'description', 'poster')

class RatingForm(forms.ModelForm):
    pass