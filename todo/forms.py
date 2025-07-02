from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # fields = '__all__'
        exclude = ['user', 'is_completed']
        labels = {
            'name': 'Name',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder':'e.g Study Django', 'class':'form-control'}),
        }