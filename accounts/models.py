from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


class CustomUser(AbstractUser):
    phone_number = models.CharField(validators=[MinLengthValidator(11)], max_length=11, blank=True, null=True)


class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')

    postal_code = models.CharField(validators=[MinLengthValidator(10)], max_length=10, verbose_name=_('Postal Code'))
    address = models.TextField()
