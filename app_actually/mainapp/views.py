import random

from django.shortcuts import render

from basketapp.models import Basket
from .models import Product, ProductCategory
from django.shortcuts import get_object_or_404


# Контролер задается функцией

def index(request):  # В качестве аргумента идет request
    context = {
        'title': 'Главная',
        'products': Product.objects.all(),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', context=context)  # Возвращается рендер из папки\


def contact(request):
    context = {
        'title': 'Контакты',
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', context=context)


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_product(hot_product):
    products_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return products_list


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return None


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()
    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {
                'name': 'все',
                'pk': 0
            }
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)
        context = {
            'links_menu': links_menu,
            'title': 'Продукты',
            'products': products_list,
            'category': category_item,
            'basket': get_basket(request.user)
        }
        return render(request, 'mainapp/products_list.html', context=context)
    hot_product = get_hot_product()
    same_products = get_same_product(hot_product)
    context = {
        'links_menu': links_menu,
        'title': 'Продукты',
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/products.html', context=context)


def main(request):
    title = 'Главная'
    products = Product.objects.all()[:4]

    content = {'title': title, 'products': products}
    return render(request, 'mainapp/index.html', content)

def product(request, pk):
    links_menu = ProductCategory.objects.all()
    context = {
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
        'links_menu': links_menu
    }
    return render(request, 'mainapp/product.html', context)
