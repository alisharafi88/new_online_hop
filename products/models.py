from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.utils.translation import gettext as _

from ckeditor.fields import RichTextField
from colorfield.fields import ColorField

from accounts import models as account


class ProductsCategory(models.Model):
    STATUS_CHOICES = (
        ('parent',),
        ('child',),
    )
    title = models.CharField(_('Title'), max_length=50)
    description = RichTextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child', blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0], max_length=1)

    @property
    def status(self):
        if self.parent:
            return self.STATUS_CHOICES[1]
        return self.STATUS_CHOICES[0]

    def __str__(self):
        if self.parent:
            return f'{self.parent}: {self.title}'
        else:
            return self.title


class Shop(models.Model):
    name = models.CharField(max_length=50)
    description = RichTextField(blank=True, null=True)


class Product(models.Model):
    PERCENT_CHOICE = ()
    for i in range(101):
        PERCENT_CHOICE += ((i, i),)

    category = models.ManyToManyField(verbose_name=_('Category'), to=ProductsCategory, related_name='products')

    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    title = models.CharField(_('Title'), max_length=50)
    description = RichTextField(verbose_name=_('Description'))
    slug = models.SlugField(allow_unicode=True)

    og_price = models.DecimalField(_('Original Price'), default=0, max_digits=6, decimal_places=2)
    discount_percent = models.PositiveIntegerField(_('Discount Percent'), choices=PERCENT_CHOICE, default=0)
    is_discount = models.BooleanField(default=False)
    discounted_price = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField(_('Total Price'), default=0)

    main_cover = models.ImageField(upload_to='covers/%y/%m/%d/main-cover')

    is_active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    average_rate = models.FloatField(default=0)

    @property
    def is_discount(self):
        if self.discount_percent:
            return True
        else:
            return False

    @property
    def average_rate(self):
        if self.comments.exists():
            rated_list = []
            for comment in self.comments.all():
                rated_list.append(int(comment.rate))
            return sum(rated_list)/len(rated_list)
        else:
            return 0

    @property
    def discounted_price(self):
        return (self.og_price * self.discount_percent) / 100

    @property
    def total_price(self):
        return self.og_price - self.discounted_price

    def __str__(self):
        return f'{self.title}: {self.category}'

    def get_absolute_url(self):
        return reverse('products:product_detail', args=(self.pk, self.slug))


class ProductRelated(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='related')

    field_name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.field_name}: {self.value}'


class FilesProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='covers/%y/%m/%d/related-cover')


class ProductSize(models.Model):
    CHOOSE_SIZE = (
        ('Extra Small', 'XS'),
        ('Small', 'S'),
        ('Medium', 'M'),
        ('Large', 'L'),
        ('Extra Large', 'XL'),
        ('Double Large', 'XXL'),
        ('Triple Large', 'XXXL'),
    )
    size = models.CharField(max_length=20, choices=CHOOSE_SIZE, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.size


class ProductColor(models.Model):
    color = models.CharField(max_length=120)
    color_code = ColorField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.color


class Variants(models.Model):
    COLOR_SIZE = (
        ('color', 'color'),
        ('size', 'size'),
    )
    color_or_size = models.CharField(choices=COLOR_SIZE, max_length=5)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.color_or_size == 'color':
            self.size = None
        else:
            self.color = None
        super(Variants, self).save(*args, **kwargs)

    def __str__(self):
        if self.color_or_size == 'color':
            return f'{self.color.color}, {self.color.color_code}'
        else:
            return self.size.size


class ProductComment(models.Model):
    RATE_CHOICES = [
        (1, _('very bad')),
        (2, _('bad')),
        (3, _('normal')),
        (4, _('good')),
        (5, _('very good')),

    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(account.CustomUser, on_delete=models.CASCADE, related_name='comments')

    text = models.CharField(max_length=500, verbose_name=_('Text'))
    rate = models.IntegerField(choices=RATE_CHOICES, verbose_name=_('Rate'))

    is_active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('Created On'))

    def __str__(self):
        return f'{self.rate}-{self.user}'


class ProductLike(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(account.CustomUser, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.user} likes, {self.product}'
