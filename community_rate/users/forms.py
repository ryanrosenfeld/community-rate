from django import forms
import pytz


class UpdateInfoForm(forms.Form):
    username = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': True})
    )
    email = forms.EmailField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fav_quote = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    about_me = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )


class profileSetupForm(forms.Form):
    fav_quote = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
    about_me = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    prof_pic = forms.FileField(widget=forms.ClearableFileInput(attrs={'id': 'wizard-picture'}))
    tz = forms.ChoiceField(
        required=True,
        choices=[(x, x) for x in pytz.common_timezones],
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class UpdateProfilePicForm(forms.Form):
    file = forms.FileField()
