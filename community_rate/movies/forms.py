from django import forms


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


class SearchForm(forms.Form):
    search = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Search', 'class': 'form-control'})
    )
