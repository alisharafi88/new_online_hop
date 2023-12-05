from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(validators=[MinLengthValidator(11)], max_length=11, blank=True, null=True)
