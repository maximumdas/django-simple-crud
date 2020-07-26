from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class RegisterUser(UserCreationForm):
    name = forms.CharField(label="Name", max_length=200, required=False)
    email = forms.EmailField(label="Email", max_length=200)
    # password = forms.CharField(label="Password", max_length=50)
    # Image field

    class Meta:
        model = User
        fields = [ "email", "name", "password1", "password2"]
