import weasyprint
from celery import shared_task
from django.core.mail import EmailMessage
from orders.models import Order
from io import BytesIO
from django.template.loader import render_to_string
from django.conf import settings


@shared_task
def payment_completed(order_id):
    """
        Задание по отправке уведомления по электронной
        почте при успешном оплата заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Yahoo Store - номер счета-фактуры {order.id}'
    message = 'Пожалуйста, ознакомьтесь с прилагаемым счетом-фактурой за вашу\
        недавнюю покупку.'
    email = EmailMessage(
        subject,
        message,
        'admin@yahoostore.com',
        [order.email]
    )
    # Сгенирорвать PDF
    html = render_to_string(
        'orders/order/pdf.html',
        {
            'order': order
        }
    )
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(
        out,
        stylesheets=stylesheets
    )
    # Прикрепить PDF-Файл
    email.attach(
        f'Заказ_{order.id}.pdf',
        out.getvalue(),
        'application/pdf'
    )
    # Отправить электронное письмо
    email.send()
