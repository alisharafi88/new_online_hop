from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import OrderForm
from cart.cart import Cart


class OrderView(View):
    form_class = OrderForm

    def get(self, request):
        form = OrderForm()
        cart = Cart(request)
        if len(cart) == 0:
            messages.warning(request, _('You can not proceed to checkout page because your cart is empty.'))
            return redirect('products:product_list')
        return render(request, 'orders/order.html', {'form': form, 'cart': cart})

