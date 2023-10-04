from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class UserRegisterForm(UserCreationForm):
    """
    Form for registering a new user.

    Attributes:
        email (EmailField): The email of the user.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating an existing user's details.

    Attributes:
        email (EmailField): The email of the user.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating a user's profile image.
    """
    class Meta:
        model = Profile
        fields = ['image']


class SubscribeForm(forms.Form):
    """
    Form for subscribing to another user.

    Attributes:
        followed_user (CharField): Username of the user to be followed.
    """
    followed_user = forms.CharField(
        label=False,
        widget=forms.TextInput()
    )
