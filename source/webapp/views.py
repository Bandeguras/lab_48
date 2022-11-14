from django.shortcuts import render, get_object_or_404, redirect
from webapp.models import Products
# Create your views here.


def index_view(request):
    products = Products.objects.order_by('name', 'category')
    context = {'products': products}
    return render(request, 'index.html', context)


def product_view(request, pk):
    product = get_object_or_404(Products, pk=pk)
    context = {'product': product}
    return render(request, 'view.html', context)