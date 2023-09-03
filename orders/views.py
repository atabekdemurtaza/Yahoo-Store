from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from .models import OrderItem
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # Очищаем корзину
            cart.clear()
            # Запускаем асинхронное задание
            order_created.delay(order.id)

            """template_name = 'orders/order/created.html'
            context = {
                'order': order
            }
            return render(
                request,
                template_name,
                context
            )"""
            request.session['order.id'] = order.id
            # Перенавправляем к платежу
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()

    template_name = 'orders/order/create.html'
    context = {
        'cart': cart,
        'form': form
    }
    return render(
        request,
        template_name,
        context
    )
