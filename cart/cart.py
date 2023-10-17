import copy

from products.models import Product


class Cart:
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.request = request
        self.session = request.session

        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, replace=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        if replace:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        products_ids = self.cart.keys()

        products = Product.objects.filter(id__in=products_ids)

        cart = copy.deepcopy(self.cart)

        for product in products:
            cart[str(product.id)]['product_obj'] = product
        for item in cart.values():
            item['total_price'] = item['product_obj'].total_price * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.save()

    # def get_total_price(self):
    #     product_ids = self.cart.keys()
    #
    #     return sum(item['quantity'] * item['product_obj'].price for item in self.cart.values())
    def get_total_price(self):
        return sum(item['quantity'] * item['product_obj'].total_price for item in self)
