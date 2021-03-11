from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Post, Comment, PostRating

# make emails unique
User._meta.get_field('email')._unique = True


# registration form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # ensure emails end in exeter.ac.uk
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
        fields = ['study_year', 'tc']


# edit user form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    # ensure emails end in exeter.ac.uk
    def clean_email(self):
        e = self.cleaned_data.get("email")
        if not "exeter.ac.uk" in e:
            raise forms.ValidationError("You must sign up with an exeter.ac.uk email address.")
        return e

    class Meta:
        model = User
        fields = ['username', 'email']


# form for changing the profile picture
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


# form for adding a comment to a post
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


# form for showing a user's total points in their profile
class ProfileaddPoints(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['points']


# form for rating the posts
class RatePostForm(forms.ModelForm):
    class Meta:
        model = PostRating
        fields = ['rating']