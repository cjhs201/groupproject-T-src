from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    study_year = forms.IntegerField(min_value=1)

    class Meta:
        model = User
        fields = ['username', 'email', 'study_year', 'password1', 'password2']