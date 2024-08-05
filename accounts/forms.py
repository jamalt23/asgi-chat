from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import User

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'placeholder' : 'Password*',
            }))

    password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'placeholder' : 'Confirm password*',
             }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'id': 'username', 'placeholder': 'Your username'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Your email adress'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'placeholder' : 'Enter your username',
            }))

    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'placeholder' : 'Enter your password',
             }))

    class Meta:
        model = User
        fields = ['username', 'password']