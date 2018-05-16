from django.forms import ModelForm
from django import forms
from .models import Hash


class HashForm(ModelForm):

    value = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'required': 'required',
            'placeholder': 'Enter hash',
            'aria - describedby':  'emailHelp'
        }
    ))

    user_email = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'required': 'required',
            'placeholder': 'Enter email',
            'aria - describedby': 'emailHelp'
        }
    ))

    class Meta:
        model = Hash
        fields = ['value', 'user_email']
