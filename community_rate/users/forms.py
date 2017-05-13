from django import forms

class EditProfileForm(forms.Form):
	# TODO: confirm the maximum lengths with Django's documentation
	username = forms.CharField(label='username', max_length=100, required=False)
	first_name = forms.CharField(label='first_name', max_length=100, required=False)
	last_name = forms.CharField(label='last_name', max_length=100, required=False)
	email = forms.EmailField(label='email', required=False)

	country = forms.CharField(label='country', max_length=100, required=False)
	city = forms.CharField(label='city', max_length=100, required=False)
	postal = forms.CharField(label='postal', max_length=6, required=False)

	bio = forms.CharField(label='bio', max_length=500, required=False)
