from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(label='Username', max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Username'}))
    password = forms.CharField(label="Confirm Password", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Enter Password'}))
    conPassword = forms.CharField(label="Confirm Password", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Confirm Password'}))
