from django.contrib import admin
from django.utils.translation import gettext as _

from .models import ProductsCategory, Product, ProductSize, ProductColor, FilesProduct, Variants, ProductRelated, Shop, ProductComment, ProductLike


class ProductsVariantsInline(admin.TabularInline):
    model = Variants
    extra = 1


class ProductFileInline(admin.TabularInline):
    model = FilesProduct
    extra = 1


class ProductRelatedInline(admin.TabularInline):
    model = ProductRelated
    extra = 1


class ProductCommentInline(admin.StackedInline):
    model = ProductComment
    extra = 1


@admin.register(ProductsCategory)
class ProductsCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_active']
    list_filter = ['created_on']
    ordering = ['created_on']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("category", "title", "description", "slug", "average_rate")}),
        (_("Price"), {"fields": ("og_price", "discount_percent", "is_discount")}),
        (_("main_cover"), {"fields": ("main_cover",)}),
        (_('activity'), {'fields': ('is_active',)}),
    )
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'updated_on', 'total_price', 'is_active', 'average_rate')
    add_fieldsets = fieldsets
    inlines = (ProductsVariantsInline, ProductFileInline, ProductRelatedInline, ProductCommentInline)


admin.site.register(ProductSize)
admin.site.register(ProductColor)
admin.site.register(ProductRelated)
admin.site.register(Shop)
admin.site.register(ProductLike)
