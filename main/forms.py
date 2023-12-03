from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Write yout task here...'
    }))
    class Meta:
        model = Task
        fields = ['name']