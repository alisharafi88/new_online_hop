from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

from products.models import Product


def validate_postal_code(value):
    value_str = str(value)
    if len(value_str) != 10:
        raise ValidationError(_("Phone number`s length should be '11' "))


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='orders')

    receiver = models.CharField(verbose_name=_('Receiver name'), max_length=50)
    receiver_phone_number = models.CharField(validators=[MinLengthValidator(11)], max_length=11, blank=True, null=True)

    order_note = models.CharField(max_length=200)

    address = models.TextField()

    is_paid = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}, {self.updated_on}.'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='ordered')

    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product.title}*{self.quantity}, {self.price}.'
