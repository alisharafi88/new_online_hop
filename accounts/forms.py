from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, UsernameField
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    pass


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"
        field_classes = {"username": UsernameField}


