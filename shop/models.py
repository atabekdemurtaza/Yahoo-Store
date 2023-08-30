from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Название', max_length=255)
    slug = models.SlugField('Слаг', max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категорию'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category',
            args=[self.slug]
        )


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField('Название', max_length=255)
    slug = models.SlugField('Слаг', max_length=255)
    image = models.ImageField(
        'Картинка',
        upload_to='products/%Y/%m/%d',
        null=True,
        blank=True
    )
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    available = models.BooleanField('Наличие', default=True)
    created = models.DateTimeField('Создание', auto_now_add=True)
    updated = models.DateTimeField('Изменение', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Продукты'
        verbose_name = 'Продукт'
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]

    def get_absolute_url(self):
        return reverse(
            'shop:product_detail',
            args=[self.id, self.slug]
        )
