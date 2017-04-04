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


class SearchForm(forms.Form):
    search = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Search', 'class': 'form-control'})
    )


class ReviewForm(forms.Form):
    rating = forms.ChoiceField(
        choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)],
        label='Rating',
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'rating-field'})
    )
    reaction = forms.CharField(
        label='Reaction',
        widget=forms.TextInput(attrs={'id': 'reaction-field'})
    )
    thoughts = forms.CharField(
        label="Thoughts",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'id': 'thoughts-field'})
    )