from django import forms
from django.core.exceptions import ValidationError
from .models import SiteUser


class LoginForm(forms.Form):
    username = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'lg_username',
                                      'name': 'lg_username'}),
    )
    password = forms.CharField(
        label='',
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'lg_password',
                                          'name': 'lg_password'})
    )


class SignupForm(forms.Form):
    first_name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'first name', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'last name', 'class': 'form-control'})
    )
    email = forms.EmailField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'email', 'class': 'form-control', 'type': 'email'}),
        error_messages={'invalid': 'The email provided is already in use'}
    )
    username = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-control'}),
        error_messages={'invalid': 'The username provided is unavailable'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control', 'minLength': '6'}),
        label='',
        error_messages={'invalid': 'The two passwords provided don\'t match'}
    )
    conf_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'confirm password', 'class': 'form-control',
                                          'minLength': '6'}),
        label='',
    )

    def clean_conf_password(self):
        password = self.cleaned_data['password']
        conf_password = self.cleaned_data['conf_password']
        if password != conf_password:
            raise ValidationError(self.fields['password'].error_messages['invalid'])
        return password

    def clean_username(self):
        username = self.cleaned_data['username']
        users = SiteUser.objects.filter(username=username)
        if len(users) > 0:
            raise ValidationError(self.fields['username'].error_messages['invalid'])
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        users = SiteUser.objects.filter(email=email)
        if len(users) > 0:
            raise ValidationError(self.fields['email'].error_messages['invalid'])
        return email
