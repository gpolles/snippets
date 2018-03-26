from django.forms import ModelForm
from .models import *
from django import forms

class Html5DateInput(forms.DateInput):
    input_type = 'date'

class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        fields = ['title', 'content', 'description', 'language']
