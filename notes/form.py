from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(label='Username', max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Username'}))
    password = forms.CharField(label="Confirm Password", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Enter Password'}))
    conPassword = forms.CharField(label="Confirm Password", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Confirm Password'}))


class UpdateForm(forms.Form):
    prev_pwd = forms.CharField(label="Current Password", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Type your current password'}))
    new_pwd = forms.CharField(label="New Password", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Enter New Password'}))
    confirm_pwd = forms.CharField(label="Confirm Password", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Confirm Password'}))
