from django.urls import path
from .views import order_create, admin_order_detail, admin_order_pdf

app_name = 'orders'

urlpatterns = [
    path(
        route='create/',
        view=order_create,
        name='order_create'
    ),
    path(
        route='admin/order/<int:order_id>/',
        view=admin_order_detail,
        name='admin_order_detail'
    ),
    path(
        route='admin/order/<int:order_id>/pdf/',
        view=admin_order_pdf,
        name='admin_order_pdf'
    ),
]
