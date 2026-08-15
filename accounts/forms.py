from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False, max_length=20)

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
