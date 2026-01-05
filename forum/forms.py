from django import forms
from .models import Thread

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }