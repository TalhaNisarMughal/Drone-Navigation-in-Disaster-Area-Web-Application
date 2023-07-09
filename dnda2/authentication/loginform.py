from django.contrib.auth.forms import AuthenticationForm

from django import forms
class loginform(AuthenticationForm):
    username=forms.CharField(label="User Name",widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    