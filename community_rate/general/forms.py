from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.bootstrap import StrictButton


class LoginForm(forms.Form):
    username = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-control', 'id': 'lg_username',
                                      'name': 'lg_username'}),
    )
    password = forms.CharField(
        label='',
        max_length=100,
        widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control', 'id': 'lg_password',
                                          'name': 'lg_password'})
    )
    remember = forms.BooleanField(
        initial=False,
        required=False,
        widget=forms.CheckboxInput(attrs={'id': 'lg_remember'}),
    )
    # def __init__(self, *args, **kwargs):


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
        widget=forms.TextInput(attrs={'placeholder': 'email', 'class': 'form-control'})
    )
    username = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'password', 'class': 'form-control'}),
        label='',
    )
    conf_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'confirm password', 'class': 'form-control'}),
        label='',
    )
