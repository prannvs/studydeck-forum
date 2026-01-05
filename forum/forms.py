from django import forms
from .models import Thread

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'category', 'course_tag', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter thread title'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'course_tag': forms.Select(attrs={'class': 'form-select'}), # Add styling for the dropdown
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your content here...'}),
        }