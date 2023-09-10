from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Coupon(models.Model):
    code = models.CharField('Код', max_length=50, unique=True)
    valid_from = models.DateTimeField('Действителен с')
    valid_to = models.DateTimeField('Действителен до')
    discount = models.IntegerField(
        'Скидка',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        help_text='Процент от (0 до 100)'
    )
    active = models.BooleanField(
        'Активен'
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = 'Купоны'
        verbose_name = 'Купон'
