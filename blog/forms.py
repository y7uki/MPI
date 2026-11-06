from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['post', 'subject', 'text']
        widgets = {
            'subject': forms.TextInput(attrs={'style': 'width: 100%; padding: 8px; margin-bottom: 10px;', 'placeholder': 'Тема комментария (до 100 символов)'}),
            'text': forms.Textarea(attrs={'style': 'width: 100%; padding: 8px; height: 80px;', 'placeholder': 'Текст комментария (до 500 символов)'}),
            'post': forms.Select(attrs={'style': 'width: 100%; padding: 8px; margin-bottom: 10px;'}),
        }