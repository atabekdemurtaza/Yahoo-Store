import csv
import datetime
from django.contrib import admin
from .models import Order, OrderItem
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'Закрепить; тип файла={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]

    # Записываем первую строку  с информацией заголовка
    writer.writerow([field.verbose_name for field in fields])
    # Записываем строк данных
    for obj in queryset:
        data_row = list()
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Вывести как CSV'


def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f"<a href='{url}'>Просмотр</a>")


def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f"<a href='{url}'>PDF</a>")


order_pdf.short_description = 'Счет-фактура'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'address',
        'postal_code',
        'city',
        'created',
        'updated',
        order_detail,
        order_pdf
    ]
    list_filter = ['created', 'updated', 'paid']
    inlines = [
        OrderItemInline,
    ]
    actions = [export_to_csv]
