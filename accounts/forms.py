from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser, UserAddress


class CustomUserCreationForm(UserCreationForm):
    pass


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email']


class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['receiver', 'receiver_phone_number', 'postal_code', 'address']
