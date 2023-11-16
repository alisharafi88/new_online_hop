from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product, ProductLike, ProductsCategory, ProductComment
from .forms import ProductCommentForm


class ProductListView(View):
    def get(self, request):
        products = Product.objects.prefetch_related('comments').filter(is_active=True)
        categories = ProductsCategory.objects.prefetch_related('products').filter(products__in=products,
                                                                                  products__is_active=True).distinct()
        return render(
            request,
            'products/home.html',
            {'products': products, 'categories': categories}
        )


class ProductDetailView(View):
    def get(self, request, product_pk, product_slug):
        comment_form = ProductCommentForm()
        product = get_object_or_404(Product.objects.prefetch_related('comments', 'category', 'variants', 'related', 'files').select_related('shop').filter(is_active=True),
                                    pk=product_pk, slug=product_slug)

        comments = ProductComment.objects.prefetch_related('user').filter(product=product, is_active=True)

        p_category = ProductsCategory.objects.prefetch_related('products').filter(products=product).distinct()

        is_liked = False
        if request.user.is_authenticated:
            vote = ProductLike.objects.filter(product=product, user=request.user)
            if vote.exists():
                is_liked = True
        return render(request, 'products/product_detail.html',
                      {'product': product, 'category_products': p_category, 'comment_form': comment_form,
                       'is_liked': is_liked, 'comments': comments})


class ProductCommentView(LoginRequiredMixin, View):
    def post(self, request, product_pk):
        product = get_object_or_404(Product, pk=product_pk)
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            messages.success(request, _('You sent your comment successfully'), 'success')
            return redirect('products:product_detail', product_pk, product.slug)
        messages.error(request, _('Somthing wrong happened. please try again!'), 'danger')
        return redirect('products:product_detail', product_pk, product.slug)


class ProductLikeView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next', None)
        return super().setup(request, *args, **kwargs)

    def get(self, request, product_pk):
        product = get_object_or_404(Product, pk=product_pk)
        like = ProductLike.objects.filter(product=product, user=request.user)
        if like.exists():
            pass
        else:
            ProductLike.objects.create(product=product, user=request.user)
        if self.next:
            return redirect(self.next)
        return redirect('products:product_detail', product_pk, product.slug)


class ProductDislikeView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next', None)
        return super().setup(request, *args, **kwargs)

    def get(self, request, product_pk):
        product = get_object_or_404(Product, pk=product_pk)
        like = ProductLike.objects.filter(product=product, user=request.user)
        if like.exists():
            like.delete()
        if self.next:
            return redirect(self.next)
        return redirect('products:product_detail', product_pk, product.slug)


class CategoryListView(View):
    def get(self, request, category_pk):
        category = get_object_or_404(ProductsCategory, pk=category_pk)
        return render(request, 'products/category_list.html', {'category': category})
