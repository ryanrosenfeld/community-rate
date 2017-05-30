from django import forms


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

# class EditProfileForm(forms.Form):
# 	# TODO: confirm the maximum lengths with Django's documentation
# 	username = forms.CharField(label='username', max_length=100, required=False)
# 	first_name = forms.CharField(label='first_name', max_length=100, required=False)
# 	last_name = forms.CharField(label='last_name', max_length=100, required=False)
# 	email = forms.EmailField(label='email', required=False)
#
# 	country = forms.CharField(label='country', max_length=100, required=False)
# 	city = forms.CharField(label='city', max_length=100, required=False)
# 	postal = forms.CharField(label='postal', max_length=6, required=False)
#
# 	bio = forms.CharField(label='bio', max_length=500, required=False)
# 	photo = forms.FileField(label='photo', required=False)
#


class UpdateProfilePicForm(forms.Form):
    file = forms.FileField()
