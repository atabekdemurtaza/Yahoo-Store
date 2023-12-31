from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from cart.forms import CartAddProductForm
from .recommender import Recommender


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(
            Category,
            slug=category_slug
        )
        products = products.filter(category=category)

    context = {
        'category': category,
        'products': products,
        'categories': categories
    }
    template_name = 'shop/product_list.html'

    return render(
        request,
        template_name,
        context
    )


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    cart_product_form = CartAddProductForm
    r = Recommender()
    recommended_products = r.suggest_product_for([product], 4)
    template_name = 'shop/product_detail.html'

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'recommended_products': recommended_products
    }
    return render(
        request,
        template_name,
        context
    )
