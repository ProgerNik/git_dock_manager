# documents/forms.py
from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'content') # Автор будет назначаться автоматически во view
        widgets = { # Добавим немного стилей для полей формы
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }