from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, UsernameField
from django import forms

from .models import CustomUser, UserAddress


class CustomUserCreationForm(UserCreationForm):
    pass


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"
        field_classes = {"username": UsernameField}


class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['receiver', 'receiver_phone_number', 'postal_code', 'address']
