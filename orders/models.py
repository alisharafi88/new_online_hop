from django.db import models
from django.conf import settings

from accounts.models import UserAddress
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='orders')

    address = models.ForeignKey(UserAddress, on_delete=models.DO_NOTHING, related_name='orders')
    order_note = models.CharField(max_length=200)

    is_paid = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}, {self.updated_on}.'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='ordered')

    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.title}*{self.quantity}, {self.price}.'
