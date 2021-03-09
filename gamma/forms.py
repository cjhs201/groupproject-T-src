from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Post, Comment

# make emails unique
User._meta.get_field('email')._unique = True

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    def clean_email(self):
        e = self.cleaned_data.get("email")
        if not "exeter.ac.uk" in e:
            raise forms.ValidationError("You must sign up with an exeter.ac.uk email address.")
        return e

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['study_year']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    def clean_email(self):
        e = self.cleaned_data.get("email")
        if not "exeter.ac.uk" in e:
            raise forms.ValidationError("You must sign up with an exeter.ac.uk email address.")
        return e

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rating']

class ProfileaddPoints(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['points']