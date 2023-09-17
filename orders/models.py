from django.db import models
from shop.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator
from coupons.models import Coupon
from decimal import Decimal
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    email = models.EmailField(_('email'))
    address = models.CharField(_('address'), max_length=50)
    postal_code = models.CharField(_('postal code'), max_length=50)
    city = models.CharField(_('city'), max_length=50)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        verbose_name=_('coupon'),
        blank=True,
        null=True
    )
    discount = models.IntegerField(
        _('discount'),
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        help_text='Процент от (0 до 100)',
        default=0
    )
    paid = models.BooleanField(_('paid'), default=False)

    def __str__(self):
        return f'Заказ #{self.id}'

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name_plural = _('Orders')
        verbose_name = _('Order')

    def get_total_cost(self):
        total_cost = self.get_total_price_before_discount()
        return total_cost - self.get_discount()

    def get_total_price_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_discount(self):
        total_cost = self.get_total_price_before_discount()
        if self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Товар'
    )
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(
        'Количество',
        default=1
    )

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
