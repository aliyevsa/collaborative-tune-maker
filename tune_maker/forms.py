from django import forms
from django.contrib.auth.models import User
from .models import *

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', required=True)

    def clean(self):
        cleaned_data = super().clean()
        submitted_username = cleaned_data.get('username')
        if not User.objects.filter(username=submitted_username).exists():
            raise forms.ValidationError('User with the username ' + submitted_username + ' does not exist.')
        else:
            cleaned_data['username'] = User.objects.get(username=submitted_username)

        return cleaned_data

class ProjectForm(forms.Form):
    name = forms.CharField(label='Project Name', max_length=64, initial='New Project')
    length = forms.IntegerField(label='Project Length', initial=16)
    collaborator = forms.CharField(label='Collaborator Username', max_length=16, required=False)

    def clean(self):
        cleaned_data = super().clean()
        collaborator_username = cleaned_data.get('collaborator')
        if collaborator_username:
            if not User.objects.filter(username=collaborator_username).exists():
                raise forms.ValidationError('User with the username ' + collaborator_username + ' does not exist.')
            else:
                cleaned_data['collaborator'] = User.objects.get(username=collaborator_username)
        else:
            cleaned_data['collaborator'] = None

        return cleaned_data
