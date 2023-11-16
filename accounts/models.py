from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


def validate_postal_code(value):
    value_str = str(value)
    if len(value_str) != 10:
        raise ValidationError(_("Phone number`s length should be '11' "))


class CustomUser(AbstractUser):
    phone_number = models.CharField(validators=[MinLengthValidator(11)], max_length=11, blank=True, null=True)


class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')

    receiver = models.CharField(verbose_name=_('Receiver name'), max_length=50)
    receiver_phone_number = models.CharField(validators=[MinLengthValidator(11)], max_length=11, blank=True, null=True)
    postal_code = models.PositiveIntegerField(verbose_name=_('Postal Code'), validators=[validate_postal_code])
    address = models.TextField()
