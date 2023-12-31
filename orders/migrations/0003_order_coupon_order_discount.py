# Generated by Django 4.1.10 on 2023-09-10 08:13

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0002_alter_coupon_options_and_more'),
        ('orders', '0002_alter_order_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coupons.coupon', verbose_name='Купон'),
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.IntegerField(default=0, help_text='Процент от (0 до 100)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Скидка'),
        ),
    ]
