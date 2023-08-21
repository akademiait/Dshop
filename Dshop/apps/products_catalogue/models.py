from django.db import models
from django.utils.text import slugify


class CatalogueItemModel(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, editable=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # for creating urls use {% url "url-name" item.slug item.pk %}
        # path('<slug:slug>-<int:pk>/', NoteDetailView.as_view(), name='note_details'),
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Category(CatalogueItemModel):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_last_30_days = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    short_description = models.TextField()
    full_description = models.TextField()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/')
    is_featured = models.BooleanField(default=False)
