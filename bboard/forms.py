from django.forms import ModelForm
from django import forms

from bboard.models import Bb
from .models import Task

class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')

# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ['title', 'description', 'priority', 'is_done']
#         widgets = {
#             'title':forms.TextInput(attrs={'class':'form-control'}),
#             'description':forms.Textarea(attrs={'class':'form-control', 'rows': 4}),
#             'priority':forms.NumberInput(attrs={'class':'form-control'}),
#         }