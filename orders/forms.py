from django import forms

from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['receiver', 'receiver_phone_number', 'order_note', 'address']
