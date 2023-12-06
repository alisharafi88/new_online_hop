from django.db.models import Prefetch
from django.shortcuts import render
from django.views import View
from products.models import Product
from .forms import SearchForm


class SearchProducts(View):
    def get(self, request):
        search = request.GET.get('search')
        products = Product.objects.prefetch_related('comments').filter(title__icontains=search, is_active=True)
        return render(request, 'search/searched_products.html', {'products': products})
