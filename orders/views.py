from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _

from .forms import OrderForm
from .models import OrderItem
from cart.cart import Cart


class OrderView(LoginRequiredMixin, View):
    form_class = OrderForm

    def setup(self, request, *args, **kwargs):
        self.cart = Cart(request)
        return super().setup(self, request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        if len(self.cart) == 0:
            messages.warning(request, _('You can not proceed to checkout page because your cart is empty.'))
            return redirect('products:product_list')
        return render(request, 'orders/order.html', {'form': form, 'cart': self.cart})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.user = request.user
            new_order.save()
            for item in self.cart:
                OrderItem.objects.create(
                    order=new_order,
                    product=item['product_obj'],
                    quantity=item['quantity'],
                    price=item['product_obj'].total_price,
                )
            request.session['order_id'] = new_order.id
            self.cart.clear()
            messages.success(request, _('Now You have new ORDER! '), 'success')
            return redirect('accounts:profile')
        messages.error(request, _('Somthing wrong happened.'), 'danger')
        return redirect(request.META.get('HTTP_REFERER', 'orders:order'))
