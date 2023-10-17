from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext as _

from products.models import Product
from .cart import Cart
from .forms import AddToCartForm


def cart_detail_view(request):
    cart = Cart(request)

    for item in cart:
        item['replace_quantity_form'] = AddToCartForm(
            initial={
                'quantity': item['quantity'],
                'inplace': True
            }
        )

    return render(request, 'cart/cart.html', {
        'cart': cart,
    })


def add_to_cart_view(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)
    form = AddToCartForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        inplace = cleaned_data['inplace']
        cart.add(product, quantity, inplace)

    messages.success(request, _('your product added to cart successfully !'))
    return redirect(request.META.get('HTTP_REFERER'))


def remove_product_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, _('your product removed from cart successfully !'))
    return redirect(request.META.get('HTTP_REFERER', 'cart:cart_detail'))


def clear_cart_view(request):
    cart = Cart(request)
    if len(cart):
        cart.clear()
        messages.success(request, _('Now your cart is empty.'))
        return redirect('products:product_list')
    messages.error(request, _('Nothing to clear!'))
    return redirect('products:product_list')
